"""Deterministic (finite-difference) experiments E1-E4."""
import numpy as np, time, sys
from fd import Model, BASE
from common import *

XREF = (0.9, 1.0)
WIN = 2.5          # evaluation window [0, WIN]^2, away from the artificial boundary

# ---------------------------------------------------------------- E1 refinement
def e1():
    rows = []
    for Xmax in [3.0, 4.0]:
        for N0 in [61, 121, 241, 481]:
            N = int(round((N0 - 1) * Xmax / 3.0)) + 1
            if N > 500 and Xmax > 3: continue
            m = Model(N=N, Xmax=Xmax); U, stop, it = m.solve()
            b1 = arm_boundary(m, U, stop, 1)
            E1 = m.X1 > m.X2
            raw = np.array([m.x[np.argmax(stop[:, j] & E1[:, j])] if (stop[:, j] & E1[:, j]).any() else np.nan for j in range(N)])
            inw = m.x <= WIN + 1e-9
            row = dict(Xmax=Xmax, N=N, h=m.h, howard_iters=it,
                       VmG_ref=m.interp(U - m.G, *XREF), VmG_11=m.interp(U - m.G, 1, 1), VmG_22=m.interp(U - m.G, 2, 2),
                       b1_axis=float(b1[0]),
                       raw_margin_full=float(np.nanmin(raw - m.x)), raw_margin_at=float(m.x[np.nanargmin(raw - m.x)]),
                       raw_margin_win=float(np.nanmin((raw - m.x)[inw])),
                       sub_margin_win=float(np.nanmin((b1 - m.x)[inw])),
                       half={str(s): float(np.interp(s, m.x, b1) - s) for s in [1.0, 1.5, 2.0, 2.5]},
                       diag_stop_nodes=[float(v) for v in m.x[np.where(np.diag(stop))[0]]],
                       areaC_win=float(((~stop) & (m.X1 <= WIN) & (m.X2 <= WIN)).sum() * m.h ** 2))
            rows.append(row); print(row, flush=True)
            if Xmax == 3.0 and N0 == 481:
                np.savez(os.path.join(OUT, 'baseline481.npz'), x=m.x, U=U, stop=stop, b1=b1, b2=arm_boundary(m, U, stop, 2))
    save('e1_refinement', rows)

# ---------------------------------------------------------------- E2 residuals
def e2():
    rows = []
    for N in [121, 241, 481]:
        m = Model(N=N); U, stop, it = m.solve()
        res = m.residuals(U, stop)
        w = U - m.G
        # smooth-fit diagnostic: one-sided difference quotient of U-G at the last continuation node
        E1 = m.X1 > m.X2; sf = []
        for j in range(N):
            if m.x[j] > WIN: break
            ls = stop[:, j] & E1[:, j]
            if ls.any():
                i = int(np.argmax(ls)); sf.append(w[i - 1, j] / m.h)
        # Neumann residual at the axes (second-order one-sided difference)
        d1 = (-3 * U[0, :] + 4 * U[1, :] - U[2, :]) / (2 * m.h)
        d2 = (-3 * U[:, 0] + 4 * U[:, 1] - U[:, 2]) / (2 * m.h)
        res.update(N=N, h=m.h, smoothfit_max=float(np.max(sf)), neumann=float(max(np.abs(d1).max(), np.abs(d2).max())),
                   min_w_on_diag=float(np.min(np.diag(w)[(m.x > 0) & (m.x <= WIN)])))
        rows.append(res); print(res, flush=True)
    save('e2_residuals', rows)

# ---------------------------------------------------------------- E3 comparison policies
def e3(N=241):
    m = Model(N=N); U, stop, it = m.solve()
    A = (m.r * m.I - m.L).tocsr()
    win = (m.X1 <= WIN) & (m.X2 <= WIN)
    E1 = m.X1 > m.alpha * m.X2; E2 = m.X1 < m.alpha * m.X2
    out = dict(N=N, window=WIN, mean_V=float(U[win].mean()))
    rel = lambda J: (U - J) / (1 + np.abs(U))
    maps = {}
    # (a) one-sided, retained arm: stop only on the D^(2) arm of the optimum
    Jret = m.evaluate(stop & E2)
    out['one_retained'] = dict(rel=stats(rel(Jret), win), abs=stats(U - Jret, win)); maps['one_retained'] = rel(Jret)
    # (a') one-sided, re-optimised: best policy among those that never stop in closure(E1)
    Ure, stop_re, _ = m.solve(allowed=E2)
    out['one_reopt'] = dict(rel=stats(rel(Ure), win), abs=stats(U - Ure, win),
                            is_epigraph=bool(all(np.all(np.diff(stop_re[i, :].astype(int)) >= 0) for i in range(N))))
    maps['one_reopt'] = rel(Ure); maps['stop_reopt'] = stop_re
    # (b) gain-form ablation: drop the local-time reward, i.e. solve
    #     min{(r-L_h) w + Gamma_ac, w} = 0 and stop on {w = 0}
    gac = gamma_ac(m.p, m.X1, m.X2)
    zero = np.zeros_like(U)
    saved_c = m.c; m.c = gac
    wt, stop_ac, _ = m.solve(payoff=zero)
    m.c = saved_c
    Jac = m.evaluate(stop_ac)
    out['no_singular'] = dict(rel=stats(rel(Jac), win), abs=stats(U - Jac, win),
                              frac_diag_stopped=float(np.diag(stop_ac)[(m.x <= WIN)].mean()),
                              first_diag_stop=float(m.x[np.argmax(np.diag(stop_ac))]) if np.diag(stop_ac).any() else None)
    maps['no_singular'] = rel(Jac); maps['stop_ac'] = stop_ac
    # check of the gain form with the singular term kept: w = V - G
    saved_c = m.c; m.c = (A @ m.G.ravel() + saved_c.ravel()).reshape(N, N)
    wfull, stop_g, _ = m.solve(payoff=zero); m.c = saved_c
    out['gain_form_check'] = float(np.abs(wfull - (U - m.G)).max())
    # (c) payoff smoothing G_eps = alpha x2 + (y + sqrt(y^2+eps^2))/2
    sm = []
    Y = m.X1 - m.alpha * m.X2
    for eps in [0.8, 0.4, 0.2, 0.1, 0.05, 0.025]:
        Ge = m.alpha * m.X2 + 0.5 * (Y + np.sqrt(Y * Y + eps * eps))
        Ue, stop_e, _ = m.solve(payoff=Ge)
        Je = m.evaluate(stop_e)
        sm.append(dict(eps=eps, sup_payoff_gap=eps / 2, bound=eps, rel=stats(rel(Je), win), abs=stats(U - Je, win),
                       frac_diag_stopped=float(np.diag(stop_e)[m.x <= WIN].mean())))
        if eps == 0.4: maps['smooth04'] = rel(Je); maps['stop_s04'] = stop_e
        print(sm[-1], flush=True)
    out['smoothing'] = sm
    print({k: v for k, v in out.items() if k != 'smoothing'}, flush=True)
    save('e3_policies', out)
    np.savez(os.path.join(OUT, 'e3_maps.npz'), x=m.x, U=U, stop=stop, **maps)

# ---------------------------------------------------------------- E3c signed post-stopping bias
def e3c():
    rows = []
    for N in [121, 241, 481]:
        m = Model(N=N); U, stop, it = m.solve()
        A = (m.r * m.I - m.L).tocsc()
        import scipy.sparse.linalg as spla
        lu = spla.splu(A)
        gain = (A @ m.G.ravel() + m.c.ravel())            # discrete Gamma (incl. singular part)
        b1 = arm_boundary(m, U, stop, 1); b2 = arm_boundary(m, U, stop, 2)
        # extend boundaries linearly where an arm is absent inside the grid
        for d in ([-0.2, -0.1, -0.05, 0.0, 0.05, 0.1, 0.2] if N == 241 else [0.0]):
            if d == 0.0:
                st = stop
            else:
                st = ((m.X1 >= np.nan_to_num(b1, nan=1e9)[None, :] + d) & (m.X1 > m.X2 + 1e-12)) | \
                     ((m.X2 >= np.nan_to_num(b2, nan=1e9)[:, None] + d) & (m.X2 > m.X1 + 1e-12))
            J = m.evaluate(st)
            P = (m.G - J)                                   # killed potential on C_b (0 on D_b)
            F = lu.solve(gain * (~st).ravel()).reshape(N, N)  # unrestricted potential of Gamma 1_C
            B = F - P
            C = ~st & (m.X1 <= WIN) & (m.X2 <= WIN)
            rows.append(dict(N=N, shift=d, P_ref=m.interp(P, *XREF), F_ref=m.interp(F, *XREF), B_ref=m.interp(B, *XREF),
                             B_11=m.interp(B, 1, 1), B_mean_C=float(B[C].mean()), B_maxabs_C=float(np.abs(B[C]).max()),
                             F_maxabs_bdry=float(np.abs(F[st & (m.X1 <= WIN) & (m.X2 <= WIN)]).max())))
            print(rows[-1], flush=True)
    save('e3c_bias', rows)

# ---------------------------------------------------------------- E4 comparative statics
def e4(N=321, Xmax=4.0):   # same spacing h = 0.0125 as N = 241 on [0,3]; larger domain so that the
    # measurement point with G = 2 is well inside for alpha != 1
    rows = []
    cases = [('alpha', 0.7), ('alpha', 1.0), ('alpha', 1.4), ('r', 0.03), ('r', 0.08),
             ('c0', 0.005), ('c0', 0.03)] + [('rho', v) for v in [-0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8]]
    for name, val in cases:
        kw = {}
        if name == 'c0': kw['c'] = (val, 0.0, 0.0)
        else: kw[name] = val
        m = Model(N=N, Xmax=Xmax, **kw); U, stop, it = m.solve()
        a = m.alpha
        E1 = m.X1 > a * m.X2; E2 = m.X1 < a * m.X2
        win = (m.X1 <= WIN) & (m.X2 <= WIN)
        b1 = arm_boundary(m, U, stop, 1); b2 = arm_boundary(m, U, stop, 2)
        q = qval(m.p)
        # widths in Y = x1 - a x2 units at the diagonal point with G = 2
        x2s = 2.0 / a; x1s = 2.0
        d1 = float(np.interp(x2s, m.x, b1) - a * x2s)            # arm 1: Y = b1(x2) - a x2
        d2 = float(a * np.interp(x1s, m.x, b2) - x1s)            # arm 2: -Y = a b2(x1) - x1
        g1 = float(gamma_ac(m.p, x1s + 1e-9, x2s)); g2 = float(gamma_ac(m.p, x1s - 1e-9, x2s))
        pred1 = q / (2 * g1 * (1 + np.sqrt(g2 / g1))); pred2 = q / (2 * g2 * (1 + np.sqrt(g1 / g2)))
        w = U - m.G
        rows.append(dict(case=name, value=val, q=q, areaC=float((~stop & win).sum() * m.h ** 2),
                         areaD1=float((stop & E1 & win).sum() * m.h ** 2), areaD2=float((stop & E2 & win).sum() * m.h ** 2),
                         width1=d1, width2=d2, pred1=pred1, pred2=pred2, central_frac=m.frac_central,
                         premium_diag2=m.interp(w, x1s, x2s)))
        print(rows[-1], flush=True)
    save('e4_statics', rows)

if __name__ == '__main__':
    for f in sys.argv[1:]:
        t = time.time(); globals()[f](); print(f, 'done in %.1fs' % (time.time() - t), flush=True)
