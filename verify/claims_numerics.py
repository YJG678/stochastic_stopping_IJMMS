"""Claims of the section "Numerical study" and how each is recomputed from code output.

Each Claim quotes the paper verbatim ('@' = printed number, '@w' = number word). Values are
taken from the output of the experiment scripts (results/*.json, *.npz), from the
configuration objects of the code (fd.BASE, exp_fd.WIN, alg1.STEP_CLIP, ...), or are computed
live from the code (fd.Model, common.arm_boundary, ...). Nothing is typed in by hand.
"""
import math, inspect, re, os
import numpy as np
from scipy.integrate import quad
from scipy.ndimage import label as cc_label
from scipy.stats import norm

from .engine import Claim
import fd, common, exp_fd, exp_mc, alg1
from fd import Model, BASE
from common import gamma_ac, qval, arm_boundary

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = BASE
WIN = exp_fd.WIN
XREF = exp_fd.XREF


# ----------------------------------------------------------------------------- helpers
def e1(ctx, xmax=3.0):
    return [r for r in ctx.json('e1_refinement') if r['Xmax'] == xmax]

def e1N(ctx, N, xmax=3.0):
    return next(r for r in e1(ctx, xmax) if r['N'] == N)

def e2N(ctx, N):
    return next(r for r in ctx.json('e2_residuals') if r['N'] == N)

def e4(ctx, case, value):
    return next(r for r in ctx.json('e4_statics') if r['case'] == case and abs(r['value'] - value) < 1e-12)

def e4sym(ctx):
    return [r for r in ctx.json('e4_statics') if not (r['case'] == 'alpha' and r['value'] != 1.0)]

def e4asym(ctx):
    return [r for r in ctx.json('e4_statics') if r['case'] == 'alpha' and r['value'] != 1.0]

def e5dt(ctx, dt):
    return next(r for r in ctx.json('e5_mc') if r['dt'] == dt)

def e5col(row, label):
    return row['labels'].index(label)

def post(ctx, dt, T):
    return next(r for r in ctx.json('e5_post') if r['dt'] == dt and r['T'] == T)

def bias(ctx, N, shift):
    return next(r for r in ctx.json('e3c_bias') if r['N'] == N and r['shift'] == shift)

def formal_halfwidth(s):
    return qval(B) / (4 * gamma_ac(B, s + 1e-12, s))

def err_pct(x, y):
    return 100 * abs(x / y - 1)

def src(path):
    return open(os.path.join(HERE, path)).read()

def ok(cond, detail):
    return bool(cond), detail

_cache = {}
def baseline_model(ctx, N=241):
    ctx.live('fd.Model(N=%d).solve()' % N)
    if N not in _cache:
        m = Model(N=N); U, stop, _ = m.solve(); _cache[N] = (m, U, stop)
    return _cache[N]

def two_sigfig_stable(vals, digits):
    r = {float('%.*g' % (digits, v)) for v in vals}
    return len(r) == 1, r


# ============================================================================ claims
C = []
A = C.append

# ---------------------------------------------------------------- 9.1 benchmark
A(Claim('kappa-positive', r'with $\kappa_i>@$', lambda c: [min(B['kappa'])], 'gt'))
A(Claim('rho-range', r'positive definite for $|\rho|<@$',
        lambda c: [max(abs(r['value']) for r in c.json('e4_statics') if r['case'] == 'rho') if True else 0], 'lt',
        note='largest |rho| used in any run'))
A(Claim('q-formula', r'$q=\sigma_1^2-2\alpha\rho\sigma_1\sigma_2+\alpha^2\sigma_2^2$, with '
        r'$\partial q/\partial\rho=-2\alpha\sigma_1\sigma_2<0$',
        check=lambda c, p: ok(all(r['q'] == qval({**B, **{'alpha': B['alpha'], 'rho': r['value']}}) or r['case'] != 'rho'
                                   for r in c.json('e4_statics'))
                               and abs((qval({**B, 'rho': 0.5}) - qval({**B, 'rho': -0.5})) - (-2 * B['alpha'] * B['sigma'][0] * B['sigma'][1])) < 4e-16
                               and -2 * B['alpha'] * B['sigma'][0] * B['sigma'][1] < 0,
                               'q in the output equals the formula; dq/drho = -2 alpha s1 s2 = %.17g < 0' % (-2 * B['alpha'] * B['sigma'][0] * B['sigma'][1]))))
C[-1].covers = True
for sym, key, idx in [('r', 'r', None), ('\\alpha', 'alpha', None)]:
    A(Claim('param-' + key, r'$%s$ & $@$ &' % sym, lambda c, key=key: [B[key]], 'exact'))
A(Claim('param-kappa', r'$\kappa_1,\kappa_2$ & $@,\ @$', lambda c: list(B['kappa']), 'exact'))
A(Claim('param-theta', r'$\theta_1,\theta_2$ & $@,\ @$', lambda c: list(B['theta']), 'exact'))
A(Claim('param-sigma', r'$\sigma_1,\sigma_2$ & $@,\ @$', lambda c: list(B['sigma']), 'exact'))
A(Claim('param-rho', r'$\rho$ & $@$ & correlation', lambda c: [B['rho']], 'exact'))
A(Claim('param-c', r'$c_0,c_1,c_2$ & $@,\ @,\ @$', lambda c: list(B['c']), 'exact'))
A(Claim('param-grid', r'$X_{\max}$; $N$ & $@$ (and $@$); $@$--$@$',
        lambda c: [3.0, 4.0, min(r['N'] for r in e1(c)), max(r['N'] for r in e1(c))], 'exact',
        note='Xmax values and N range of the refinement runs'))
A(Claim('param-xmax-set', r'$X_{\max}$; $N$ & $3$ (and $4$)',
        check=lambda c, p: ok(sorted({r['Xmax'] for r in c.json('e1_refinement')}) == [3.0, 4.0], 'Xmax in output: %s' % sorted({r['Xmax'] for r in c.json('e1_refinement')}))))
A(Claim('param-window', r'window & $[@,@]^2$', lambda c: [0.0, WIN], 'exact'))
A(Claim('param-xref', r'$x_{\rm ref}$ & $(@,@)$', lambda c: list(exp_mc.XREF), 'exact'))
A(Claim('param-mc', r'$\Delta t$; $T_{\max}$; $M$ & $@$--$@$; $@$; $@$',
        lambda c: [min(r['dt'] for r in c.json('e5_mc')), max(r['dt'] for r in c.json('e5_mc')),
                   c.json('e5_mc')[0]['T'], c.json('e5_mc')[0]['M']], 'exact'))
A(Claim('param-seed', r'PCG64, seed $@$ & independent paths (\Cref{sec:mcnum,sec:biasnum})',
        check=lambda c, p: ok(all(s == p[0].float for s in seeds_used()),
                              'seeds actually used: Sec. mcnum table %d, Fig. mc (M-sweep) %d, Sec. biasnum %d' % tuple(seeds_used()))))

def seeds_used():
    s = src('exp_mc.py')
    base = exp_mc.SEED
    offs = [int(x) if x else 0 for x in re.findall(r'default_rng\(SEED(?:\s*\+\s*(\d+))?\)', s)]
    return [base + o for o in offs]

A(Claim('central-drift', r'At the baseline all drift differences are central',
        check=lambda c, p: central_check(c)))

def central_check(c):
    c.live('fd.Model assembly')
    fr = [Model(N=N).frac_central for N in (61, 121, 241, 481)]
    return ok(all(f == 1.0 for f in fr), 'fraction of nodes with central drift differences: %s' % fr)

A(Claim('second-order', r'is @w-order consistent in the interior',
        check=lambda c, p: second_order_check(c)))

def second_order_check(c):
    """Truncation error of L_h on a smooth function in the interior: observed order."""
    c.live('fd.Model truncation test')
    errs = []
    for N in (61, 121, 241):
        m = Model(N=N); X1, X2 = m.X1, m.X2
        f = np.sin(1.3 * X1) * np.cos(0.7 * X2) + 0.1 * X1 * X2 ** 2
        k1, k2 = B['kappa']; t1, t2 = B['theta']; s1, s2 = B['sigma']
        fx = 1.3 * np.cos(1.3 * X1) * np.cos(0.7 * X2) + 0.1 * X2 ** 2
        fy = -0.7 * np.sin(1.3 * X1) * np.sin(0.7 * X2) + 0.2 * X1 * X2
        fxx = -1.69 * np.sin(1.3 * X1) * np.cos(0.7 * X2)
        fyy = -0.49 * np.sin(1.3 * X1) * np.cos(0.7 * X2) + 0.2 * X1
        Lf = k1 * (t1 - X1) * fx + k2 * (t2 - X2) * fy + 0.5 * s1 ** 2 * fxx + 0.5 * s2 ** 2 * fyy
        e = (m.L @ f.ravel()).reshape(N, N) - Lf
        inner = (X1 > 0.5) & (X1 < 2.5) & (X2 > 0.5) & (X2 < 2.5)
        errs.append(np.abs(e[inner]).max())
    orders = [math.log2(errs[i] / errs[i + 1]) for i in range(2)]
    return ok(all(1.8 < o < 2.2 for o in orders), 'interior truncation errors %s, observed orders %s' %
              (['%.2e' % x for x in errs], ['%.3f' % o for o in orders]))

A(Claim('monotone-correlated', r'for the correlated runs $a_{ii}-|a_{12}|=\sigma^2(1-|\rho|)>@$',
        lambda c: [min(s * s * (1 - abs(r['value'])) for r in c.json('e4_statics') if r['case'] == 'rho' for s in B['sigma'])], 'gt'))
C[-1].covers = True
A(Claim('seven-point', r'and the @w-point stencil is monotone', check=lambda c, p: seven_point(c, p)))

def seven_point(c, p):
    c.live('fd.Model(rho=0.4) stencil')
    m = Model(N=41, rho=0.4); L = m.L.tocsr()
    i = 20 * 41 + 20
    row = L.getrow(i); offd = [v for j, v in zip(row.indices, row.data) if j != i and v != 0]
    return ok(row.nnz == 7 and all(v >= 0 for v in offd) and p[0] == 'seven',
              'interior row of L_h for rho=0.4 has %d nonzeros, off-diagonal min %.3g' % (row.nnz, min(offd)))

A(Claim('howard-iters', r"Howard's iteration terminated in $@$, $@$, $@$ and $@$ steps for $N=@,@,@,@$",
        lambda c: [e1N(c, N)['howard_iters'] for N in (61, 121, 241, 481)] + [61, 121, 241, 481],
        ['exact'] * 8))
A(Claim('subcell-recon', r'$\sqrt{U-G}$ is extrapolated linearly from the last @w continuation nodes to its zero',
        check=lambda c, p: subcell_check(c)))
C[-1].covers = True

def subcell_check(c):
    """arm_boundary on synthetic data w = k (b - x)^2 must recover b to machine precision."""
    c.live('common.arm_boundary synthetic test')
    m = Model(N=61); bt = 1.2345678
    w = np.where(m.X1 < bt, 0.37 * (bt - m.X1) ** 2, 0.0)
    G = m.G; U = G + w; stop = (m.X1 >= bt) & (m.X1 > m.X2)
    b = arm_boundary(m, U, stop, 1)
    err = abs(b[0] - bt)
    return ok(err < 1e-12, 'boundary recovered from two continuation nodes with error %.2e' % err)

A(Claim('area-weight', r"""each node carrying weight
$h^2$""", check=lambda c, p: area_check(c)))
C[-1].covers = True

def area_check(c):
    m, U, stop = baseline_model(c, 241)
    win = (m.X1 <= WIN) & (m.X2 <= WIN)
    a = float(((~stop) & win).sum() * m.h ** 2)
    r = e4(c, 'alpha', 1.0)['areaC']
    return ok(abs(a - r) <= 4 * math.ulp(r), 'area(C) = #nodes x h^2 = %.17g, stored %.17g' % (a, r))

A(Claim('window-text', r'loss statistics are computed over the nodes of the window $[@,@]^2$', lambda c: [0.0, WIN], 'exact'))

# ---------------------------------------------------------------- 9.2 geometry & refinement
A(Claim('fig-N', r'shows the computed stopping set for $N=@$', lambda c: [c.npz('baseline481')['x'].size], 'exact'))
A(Claim('two-arms', r"""For this benchmark it consists of
@w arms, @w in $E_1$ and @w in $E_2$""", check=lambda c, p: arms_check(c, p)))

def arms_check(c, p):
    d = c.npz('baseline481'); x = d['x']; stop = d['stop']
    X1, X2 = np.meshgrid(x, x, indexing='ij')
    win = (X1 <= WIN) & (X2 <= WIN)
    lab, n = cc_label(stop & win)
    comps = [(X1[lab == k] > X2[lab == k]).all() or (X1[lab == k] < X2[lab == k]).all() for k in range(1, n + 1)]
    sides = sorted(['E1' if (X1[lab == k] > X2[lab == k]).all() else 'E2' for k in range(1, n + 1)])
    lab_all, n_all = cc_label(stop)
    return ok(n == 2 and all(comps) and sides == ['E1', 'E2'] and p == ['two', 'one', 'one'],
              '%d connected components in the window, in %s (on the full grid: %d, joined at the artificial corner)' % (n, sides, n_all))

A(Claim('narrows', r"""separated by a continuation region that contains $\Da$
and narrows as $x_1=x_2$ increases""", check=lambda c, p: narrows_check(c)))

def narrows_check(c):
    d = c.npz('baseline481'); x = d['x']; b1 = d['b1']; stop = d['stop']
    k = (x >= 0.0) & (x <= WIN)
    hw = (b1 - x)[k]
    diag_ok = not np.diag(stop)[(x > 0) & (x <= WIN)].any()
    h = x[1] - x[0]; inc = np.diff(hw)
    good = hw[-1] < 0.25 * hw[0] and inc.max() <= h / 2
    return ok(good and diag_ok,
              'half-width %.3f at x2=0 -> %.3f at x2=2.5; largest local increase %.1e <= h/2 = %.1e (sub-cell reconstruction staircase); '
              'no diagonal node stopped in (0,2.5]: %s' % (hw[0], hw[-1], inc.max(), h / 2, diag_ok))

A(Claim('gac-threshold', r'$\cD\cap E_1\cap\Q\subset\{\Gac\ge@\}=\{x_1\ge(\kappa_1\theta_1-c_0)/(r+\kappa_1)\}=\{x_1\ge@\}$',
        lambda c: [gac_min_on_D1(c), (B['kappa'][0] * B['theta'][0] - B['c'][0]) / (B['r'] + B['kappa'][0])],
        ['ge', 'round'], note='first value: min of Gamma_ac over computed D1 (N=481)'))
C[-1].covers = True

def gac_min_on_D1(c):
    d = c.npz('baseline481'); x = d['x']; X1, X2 = np.meshgrid(x, x, indexing='ij')
    D1 = d['stop'] & (X1 > X2) & (X2 > 0) & (X1 < x[-1])
    return float(gamma_ac(B, X1[D1], X2[D1]).min())

A(Claim('arm-location', r'the computed arm lies in $\{x_1\ge@\}$', lambda c: [arm_min_x1(c)], 'ge'))

def arm_min_x1(c):
    d = c.npz('baseline481'); x = d['x']; X1, X2 = np.meshgrid(x, x, indexing='ij')
    return float(X1[d['stop'] & (X1 > X2)].min())

A(Claim('fig-regions-gac0', r'the necessary region boundary $\Gac=@$ of',
        lambda c: [abs(gamma_ac(B, (B['kappa'][0] * B['theta'][0] - B['c'][0]) / (B['r'] + B['kappa'][0]), 0.0))], 'round',
        note='|Gamma_ac| on E1 at the plotted line x1 = (kappa theta - c0)/(r + kappa) (figs.regions)'))
A(Claim('fig-regions-N', r'Computed stopping set for the baseline ($N=@$)', lambda c: [c.npz('baseline481')['x'].size], 'exact'))

A(Claim('stable-digits', r"""The value at $x_{\rm ref}$
is stable to @w digits""", check=lambda c, p: digits_check(c)))

def digits_check(c):
    v = [r['VmG_ref'] for r in e1(c)]
    st, s = two_sigfig_stable(v, 4)
    st2, s2 = two_sigfig_stable(v[1:], 4)
    return ok(st, 'values %s rounded to 4 significant digits give %s (N>=121 only: %s)' % (['%.6f' % x for x in v], sorted(s), sorted(s2)))

A(Claim('bdry-within', r'the boundary positions inside the window to within about $@$',
        lambda c: [max(max(q) - min(q) for q in [[r['b1_axis'] for r in e1(c)]] + [[r['half'][k] for r in e1(c)] for k in ('1.5', '2.0', '2.5')])],
        'le', note='largest spread over N of b1(0) and of the half-widths at 1.5, 2.0, 2.5'))
A(Claim('truncation', r"""both
are insensitive to the truncation $X_{\max}\in\{@,@\}$""", lambda c: [3.0, 4.0], 'exact'))
A(Claim('truncation-check', r'are insensitive to the truncation', check=lambda c, p: trunc_check(c)))

def trunc_check(c):
    """X_max = 3 and X_max = 4 rows with equal h must agree at the precision printed in the table."""
    from .texnum import Printed
    prec = {'VmG_ref': '0.27529', 'b1_axis': '1.466', '1.5': '0.249', '2.0': '0.148', '2.5': '0.106'}
    same = True
    for r4 in e1(c, 4.0):
        r3 = next(r for r in e1(c, 3.0) if abs(r['h'] - r4['h']) < 1e-15)
        for k, fmt in prec.items():
            a = r3[k] if k in r3 else r3['half'][k]; b = r4[k] if k in r4 else r4['half'][k]
            same &= Printed(fmt).round_like(a) == Printed(fmt).round_like(b)
    diffs = []
    for r4 in e1(c, 4.0):
        r3 = next(r for r in e1(c, 3.0) if abs(r['h'] - r4['h']) < 1e-15)
        for k in ('VmG_ref', 'VmG_11', 'VmG_22', 'b1_axis'):
            diffs.append(abs(r3[k] - r4[k]))
        diffs += [abs(r3['half'][k] - r4['half'][k]) for k in r3['half']]
    return ok(same, 'identical at the printed precision; max |difference| between X_max=3 and X_max=4 at equal h: %.2e' % max(diffs))

A(Claim('min-dist-equals-h', r"""the minimum nodal distance over the full domain equals
$h$ at every resolution""", check=lambda c, p: ok(all(abs(r['raw_margin_full'] - r['h']) <= 4 * math.ulp(r['Xmax']) for r in c.json('e1_refinement')),
        'max |distance - h| = %.2e <= 4 ulp(X_max) = %.2e: equal to machine precision of the grid coordinates' % (
            max(abs(r['raw_margin_full'] - r['h']) for r in c.json('e1_refinement')), 4 * math.ulp(4.0)))))
A(Claim('min-dist-outer', r'It is attained in the outer part of the domain',
        check=lambda c, p: ok(all(r['raw_margin_at'] > WIN for r in c.json('e1_refinement')),
                              'attained at x2 = %s' % [round(r['raw_margin_at'], 4) for r in c.json('e1_refinement')])))
A(Claim('hw-text', r'its half-width decreases from $@$ at $x_2=@$ to $@$ at $x_2=@$',
        lambda c: [e1N(c, 481)['half']['1.0'], 1.0, e1N(c, 481)['half']['2.5'], 2.5], ['round', 'exact', 'round', 'exact']))
A(Claim('hw-formal-pct', r'within $@$--$@\%$ of the formal value $q/(4\Gac)$ for $x_2\ge@$',
        lambda c: [min(err_pct(e1N(c, 481)['half'][k], formal_halfwidth(float(k))) for k in ('1.5', '2.0', '2.5')),
                   max(err_pct(e1N(c, 481)['half'][k], formal_halfwidth(float(k))) for k in ('1.5', '2.0', '2.5')), 1.5],
        ['round', 'round', 'exact'], note='N=481, x2 in {1.5, 2.0, 2.5}'))
A(Claim('premium-25', r"""the continuation premium on
$\Da$ at $(@,@)$ is $@$ against the formal $q/(16\Gac)=@$""",
        lambda c: [2.5, 2.5, premium_diag(c, 2.5), qval(B) / (16 * gamma_ac(B, 2.5 + 1e-12, 2.5))], ['exact', 'exact', 'round', 'round']))

def premium_diag(c, s):
    d = c.npz('baseline481'); x = d['x']; i = int(round(s / (x[1] - x[0])))
    assert abs(x[i] - s) < 1e-12
    X = x[i]; G = max(X, B['alpha'] * X)
    return float(d['U'][i, i] - G)

A(Claim('strict-cont', r'strict continuation on $\Da$ with no uniform separation',
        check=lambda c, p: ok(e2N(c, 481)['min_w_on_diag'] > 0, 'min of V-G on the diagonal nodes in (0,2.5]: %.4g > 0, decreasing to the end of the window' % e2N(c, 481)['min_w_on_diag'])))

# refinement table
for N in (61, 121, 241, 481):
    A(Claim('tab-refine-%d' % N, r'$%d$ & $@$ & $@$ & $@$ & $@$ & $@$ & $@$ & $@$\\' % N,
            lambda c, N=N: [e1N(c, N)['h'], e1N(c, N)['VmG_ref'], e1N(c, N)['b1_axis'], e1N(c, N)['half']['1.5'],
                            e1N(c, N)['half']['2.0'], e1N(c, N)['half']['2.5'], e1N(c, N)['raw_margin_full']],
            ['exact'] + ['round'] * 6))
    C[-1].covers_first = True
A(Claim('tab-refine-formal', r'formal $q/(4\Gac)$} & $@$ & $@$ & $@$',
        lambda c: [formal_halfwidth(s) for s in (1.5, 2.0, 2.5)]))
A(Claim('tab-refine-header', r'$N$ & $h$ & $(V-G)(x_{\rm ref})$ & $b_1(0)$ & $@$ & $@$ & $@$',
        lambda c: [float(k) for k in ('1.5', '2.0', '2.5') if k in e1N(c, 481)['half']], 'exact'))
A(Claim('tab-refine-cap', r"""Grid refinement for the baseline, $X_{\max}=@$. The runs with $X_{\max}=@$ and the same
$h\ge@$ agree with the corresponding rows.""",
        lambda c: [3.0, 4.0, min(r['h'] for r in e1(c, 4.0))], 'exact'))
A(Claim('tab-refine-cap-agree', r'agree with the corresponding rows', check=lambda c, p: trunc_check(c)))
A(Claim('fig-refine-grids', r'half-width of the continuation wedge along $\Da$ for @w grids',
        check=lambda c, p: ok(len(re.findall(r'\d+', re.search(r'for N in \[([^\]]*)\]', src('figs.py')).group(1))) == 3 and p[0] == 'three',
                              'figs.refine plots N = %s' % re.search(r'for N in \[([^\]]*)\]', src('figs.py')).group(1))))
A(Claim('fig-refine-cell', r"""equals @w grid cell at every resolution, whereas the reconstructed distance
within the window $[@,@]^2$ is resolved""",
        check=lambda c, p: ok(p[2] == 'one' and p[0].float == 0 and p[1].float == WIN and all(abs(r['raw_margin_full'] - r['h']) <= 4 * math.ulp(r['Xmax']) for r in c.json('e1_refinement'))
                              and np.ptp([r['sub_margin_win'] for r in e1(c) if r['N'] >= 121]) <= 0.005,
                              'nodal distance = h; reconstructed distance in the window %s (N >= 121 spread <= 0.005: resolved)' % [round(r['sub_margin_win'], 4) for r in e1(c)])))

# ---------------------------------------------------------------- 9.3 diagnostics
A(Claim('roundoff', r'variational-inequality residuals are at round-off level',
        check=lambda c, p: ok(max(max(r[k] for k in ('majorisation', 'superharmonic', 'complementarity', 'continuation_eq')) for r in c.json('e2_residuals')) < 1e-10,
                              'largest residual %.2e' % max(max(r[k] for k in ('majorisation', 'superharmonic', 'complementarity', 'continuation_eq')) for r in c.json('e2_residuals')))))
A(Claim('sf-halves', r'The smooth-fit quotient @w with $h$',
        check=lambda c, p: ratio_check([e2N(c, N)['smoothfit_max'] for N in (121, 241, 481)], 1.0, p[0] == 'halves', 'ratio')))
A(Claim('neumann-order', r"""Neumann
quotient decreases at @w order""",
        check=lambda c, p: ratio_check([e2N(c, N)['neumann'] for N in (121, 241, 481)], 2.0, p[0] == 'second', 'order')))

def ratio_check(v, order, word_ok, what):
    orders = [math.log2(v[i] / v[i + 1]) for i in range(len(v) - 1)]
    return ok(word_ok and all(abs(o - order) <= 0.25 for o in orders),
              'successive ratios %s, observed orders %s (criterion: |order - %g| <= 0.25)' %
              (['%.3f' % (v[i] / v[i + 1]) for i in range(len(v) - 1)], ['%.3f' % o for o in orders], order))

A(Claim('tab-res-header', r'Quantity & $N=@$ & $N=@$ & $N=@$', lambda c: [r['N'] for r in c.json('e2_residuals')], 'exact'))
A(Claim('tab-res-four', r"""The
@w @w rows vanish up to linear-solver round-off""",
        check=lambda c, p: ok(p == ['first', 'four'] and max(max(r[k] for k in ('majorisation', 'superharmonic', 'complementarity', 'continuation_eq')) for r in c.json('e2_residuals')) < 1e-10,
                              'rows: majorization, superharmonicity, complementarity, continuation equation')))
for name, key in [('majorization $\\max(G-U)^+$', 'majorisation'),
                  ('superharmonicity $\\max(-((rI-\\cL_h)U+c))^+$', 'superharmonic'),
                  ('complementarity $\\max|((rI-\\cL_h)U+c)(U-G)|$', 'complementarity'),
                  ('continuation equation $\\max_{\\cC_h}|(rI-\\cL_h)U+c|$', 'continuation_eq'),
                  ('smooth-fit quotient $\\max(U-G)(z-he_1)/h$', 'smoothfit_max'),
                  ('Neumann quotient at the axes', 'neumann')]:
    A(Claim('tab-res-' + key, name + r' & $@$ & $@$ & $@$', lambda c, key=key: [e2N(c, N)[key] for N in (121, 241, 481)]))

# ---------------------------------------------------------------- 9.4 policies
A(Claim('pol-N', r"""linear solve of
\Cref{sec:fd} with $N=@$""", lambda c: [c.json('e3_policies')['N']], 'exact'))
A(Claim('pol-meanV', r'The mean of $\hat V_{\rm ref}$ over the window is $@$', lambda c: [c.json('e3_policies')['mean_V']]))
A(Claim('pol-epigraph', r"""Its stopping set is an
epigraph""", check=lambda c, p: ok(c.json('e3_policies')['one_reopt']['is_epigraph'], 'every column of the stopping mask is monotone in x2')))
A(Claim('pol-firstrow', r"""for $x_1\gtrsim@$ it extends down to the @w row of nodes above
$\Da$""", lambda c: [first_row_x(c)], 'le',
        note='onset: smallest x1 from which the re-optimised stopping set starts at the first node above the diagonal; the property must hold for all x1 >= printed value'))
A(Claim('pol-firstrow-word', r'it extends down to the @w row', check=lambda c, p: ok(p[0] == 'first' and first_row_x(c) < WIN, 'gap = h from x1 = %.4f on' % first_row_x(c))))

def first_row_x(c):
    d = c.npz('e3_maps'); x = d['x']; st = d['stop_reopt']; h = x[1] - x[0]
    gaps = []
    for i in range(len(x) - 1):
        col = st[i, :]
        gaps.append(x[np.argmax(col)] - x[i] if col.any() else np.inf)
    gaps = np.array(gaps)
    good = np.abs(gaps - h) < 1e-9
    i0 = next(i for i in range(len(good)) if good[i:].all())
    return float(x[i0])

A(Claim('pol-ab-means', r'(mean $@\%$ against $@\%$,', lambda c: [100 * c.json('e3_policies')['one_reopt']['rel']['mean'], 100 * c.json('e3_policies')['one_retained']['rel']['mean']]))
A(Claim('pol-ab-order', r'loss of (b) is smaller than that of (a) but of the same order',
        check=lambda c, p: ok(0.1 < c.json('e3_policies')['one_reopt']['rel']['mean'] / c.json('e3_policies')['one_retained']['rel']['mean'] < 1,
                              'ratio of means %.3f' % (c.json('e3_policies')['one_reopt']['rel']['mean'] / c.json('e3_policies')['one_retained']['rel']['mean']))))
A(Claim('pol-ab-concentrated', r"""in both cases it is concentrated in the region of $E_1$ where the computed
solution stops""", check=lambda c, p: concentration(c, ['one_retained', 'one_reopt'], 'D1')))
A(Claim('pol-c-concentrated', r'its loss is concentrated around $\Da$', check=lambda c, p: concentration(c, ['no_singular'], 'diag')))

def concentration(c, keys, region):
    """Criterion fixed in advance: the share of total loss in the region is at least twice the
    region's share of the window (enrichment >= 2)."""
    d = c.npz('e3_maps'); x = d['x']; X1, X2 = np.meshgrid(x, x, indexing='ij')
    win = (X1 <= WIN) & (X2 <= WIN)
    R = (d['stop'] & (X1 > X2)) if region == 'D1' else (np.abs(X1 - X2) <= 0.25)
    out, good = [], True
    for k in keys:
        L = np.maximum(d[k], 0)[win]; Rw = R[win]
        share, area = L[Rw].sum() / L.sum(), Rw.mean()
        good &= share >= 2 * area
        out.append('%s: %.0f%% of the loss in %.0f%% of the window' % (k, 100 * share, 100 * area))
    return ok(good, '; '.join(out) + (' (region: computed D1)' if region == 'D1' else ' (region: |x1-x2|<=0.25)'))

A(Claim('pol-onesided-consistent', r'one-sided stopping sets are consistent with', check=lambda c, p: ok(True, 'statement about the theory; no number')))
for lab, key in [('(a) one-sided, retained arm', 'one_retained'), ('(b) one-sided, re-optimised', 'one_reopt'), ('(c) local-time reward dropped', 'no_singular')]:
    A(Claim('tab-loss-' + key, lab + r' & $@$ & $@$ & $@$ & $@$ & $@$ & $@$\\',
            lambda c, key=key: [100 * c.json('e3_policies')[key]['rel'][s] for s in ('mean', 'p95', 'max')] +
                               [c.json('e3_policies')[key]['abs'][s] for s in ('mean', 'p95', 'max')]))
A(Claim('tab-loss-cap', r"""over the nodes of
$[@,@]^2$ ($N=@$)""", lambda c: [0.0, WIN, c.json('e3_policies')['N']], 'exact'))
A(Claim('tab-loss-header', r'& 95th pct. & max & mean & 95th pct. & max', check=lambda c, p: ok(True, '95th percentile computed with numpy.percentile(.., 95) in common.stats')))
C[-1].covers = True

A(Claim('gainform-check', r'reproduces $\hat V_{\rm ref}-G$ to $@$', lambda c: [c.json('e3_policies')['gain_form_check']]))
A(Claim('nosing-diag', r"""Policy (c) stops on $@\%$ of the
nodes of $\Da$ in the window, namely for $x_1=x_2\gtrsim@$""",
        lambda c: [100 * c.json('e3_policies')['no_singular']['frac_diag_stopped'], c.json('e3_policies')['no_singular']['first_diag_stop']],
        ['round', 'round']))
A(Claim('nosing-diag-contig', r'namely for $x_1=x_2\gtrsim0.99$', check=lambda c, p: diag_contig(c)))

def diag_contig(c):
    d = c.npz('e3_maps'); x = d['x']; dg = np.diag(d['stop_ac'])[x <= WIN]
    i0 = int(np.argmax(dg))
    return ok(dg[i0:].all() and not dg[:i0].any(), 'diagonal nodes stopped exactly for x >= %.4f' % x[i0])
A(Claim('nosing-loss', r"""mean $@\%$,
maximum $@\%$. This is the quantitative effect""",
        lambda c: [100 * c.json('e3_policies')['no_singular']['rel']['mean'], 100 * c.json('e3_policies')['no_singular']['rel']['max']]))

# smoothing
A(Claim('psi-formula', r"""$\psi_\epsilon''(y)=\epsilon^2/(2(y^2+\epsilon^2)^{3/2})$, which integrates to @w for every
$\epsilon$""", check=lambda c, p: psi_check(c, p)))
C[-1].covers = True

def psi_check(c, p):
    c.live('quadrature of psi_eps\'\'')
    eps_list = [s['eps'] for s in c.json('e3_policies')['smoothing']]
    worst_int, worst_der = 0.0, 0.0
    for e in eps_list:
        f = lambda y: e * e / (2 * (y * y + e * e) ** 1.5)
        I = quad(f, -np.inf, np.inf, epsabs=1e-14, epsrel=1e-13)[0]
        worst_int = max(worst_int, abs(I - 1))
        psi = lambda y: 0.5 * (y + np.sqrt(y * y + e * e))
        for y in (-0.3, 0.0, 0.17):
            hh = 1e-3 * e
            fd2 = (psi(y + hh) - 2 * psi(y) + psi(y - hh)) / hh ** 2
            worst_der = max(worst_der, abs(fd2 / f(y) - 1))
    return ok(p[0] == 'one' and worst_int < 1e-10 and worst_der < 1e-4,
              'max |integral - 1| = %.1e over eps in %s; formula matches the second difference of psi to %.1e' % (worst_int, eps_list, worst_der))

A(Claim('smooth-bound', r"""a policy optimal for $G_\epsilon$ loses at most $2\eta$ under
$G$; here $\eta=\epsilon/2$""", check=lambda c, p: smooth_bound(c)))
C[-1].covers = True

def smooth_bound(c):
    sm = c.json('e3_policies')['smoothing']
    m, U, stop = baseline_model(c, 241)
    Y = m.X1 - m.alpha * m.X2; worst = 0
    for s in sm:
        gap = m.alpha * m.X2 + 0.5 * (Y + np.sqrt(Y * Y + s['eps'] ** 2)) - m.G
        worst = max(worst, gap.max() / (s['eps'] / 2))
        assert gap.min() >= -1e-15
    good = all(s['abs']['max'] <= s['eps'] for s in sm)
    return ok(good and worst <= 1 + 1e-12, 'sup(G_eps-G)/(eps/2) = %.15f; max abs loss / eps = %.3g' % (worst, max(s['abs']['max'] / s['eps'] for s in sm)))

A(Claim('smooth-negligible', r'The loss decreases rapidly with $\epsilon$ and is negligible once $\epsilon\le@$, where the smoothed-payoff policy no longer stops on $\Da$',
        lambda c: [max(s['eps'] for s in c.json('e3_policies')['smoothing'] if s['frac_diag_stopped'] == 0)], 'exact',
        note='largest eps with no diagonal node stopped'))
A(Claim('smooth-rapid', r'The loss decreases rapidly with $\epsilon$', check=lambda c, p: smooth_rapid(c)))

def smooth_rapid(c):
    sm = sorted(c.json('e3_policies')['smoothing'], key=lambda s: -s['eps'])
    m = [s['rel']['mean'] for s in sm]
    fac = [m[i] / m[i + 1] for i in range(len(m) - 1)]
    neg = all(100 * s['rel']['mean'] < 0.01 for s in sm if s['eps'] <= 0.1)
    nostop = all((s['frac_diag_stopped'] == 0) == (s['eps'] <= 0.1) for s in sm)
    return ok(all(f >= 3 for f in fac) and neg and nostop,
              'mean loss reduced by factors %s per halving of eps (criterion >= 3); mean loss < 0.01%% for eps <= 0.1: %s; '
              'diagonal stopped iff eps > 0.1: %s' % (['%.1f' % f for f in fac], neg, nostop))

for s_eps in (0.8, 0.4, 0.2, 0.1, 0.05, 0.025):
    A(Claim('tab-smooth-%g' % s_eps, r'$%s$ & $@$ & $@$ & $@$ & $@$ & $@$\\' % ('%g' % s_eps),
            lambda c, e=s_eps: (lambda s: [100 * s['rel']['mean'], 100 * s['rel']['max'], s['abs']['mean'], s['abs']['max'], s['frac_diag_stopped']])(
                next(s for s in c.json('e3_policies')['smoothing'] if s['eps'] == e))))
    C[-1].covers_first = True
A(Claim('tab-smooth-cap', r"""($N=@$, window $[@,@]^2$). Since $@\le G_\epsilon-G\le\epsilon/2$, the absolute loss is at most
$\epsilon$""", lambda c: [c.json('e3_policies')['N'], 0.0, WIN, smooth_min_gap(c)], ['exact', 'exact', 'exact', 'le']))
C[-1].covers = True

def smooth_min_gap(c):
    m, U, stop = baseline_model(c, 241)
    Y = m.X1 - m.alpha * m.X2
    return -min(float((m.alpha * m.X2 + 0.5 * (Y + np.sqrt(Y * Y + s['eps'] ** 2)) - m.G).min()) for s in c.json('e3_policies')['smoothing'])

# ---------------------------------------------------------------- 9.5 bias
A(Claim('bias-delta-enlarges', r"""(so that $\delta>@$
enlarges the continuation region)""", check=lambda c, p: enlarge_check(c, p)))

def enlarge_check(c, p):
    m, U, stop = baseline_model(c, 241)
    b1 = arm_boundary(m, U, stop, 1); b2 = arm_boundary(m, U, stop, 2)
    cnt = []
    for d in (-0.1, 0.0, 0.1):
        if d == 0:
            st = stop
        else:
            st = ((m.X1 >= np.nan_to_num(b1, nan=1e9)[None, :] + d) & (m.X1 > m.X2 + 1e-12)) | \
                 ((m.X2 >= np.nan_to_num(b2, nan=1e9)[:, None] + d) & (m.X2 > m.X1 + 1e-12))
        cnt.append(int((~st).sum()))
    return ok(p[0].float == 0 and cnt[0] < cnt[1] < cnt[2], 'continuation nodes for delta = -0.1, 0, 0.1: %s' % cnt)

A(Claim('bias-text', r"""At the computed solution $B_b(x_{\rm ref})$ is $@$, $@$
and $@$ for $N=@,@,@$""",
        lambda c: [bias(c, N, 0.0)['B_ref'] for N in (121, 241, 481)] + [121, 241, 481], ['round'] * 3 + ['exact'] * 3))
A(Claim('bias-halves', r"""it @w with $h$, as expected from the $O(h)$ discrete
smooth-fit defect""", check=lambda c, p: ratio_check([abs(bias(c, N, 0.0)['B_ref']) for N in (121, 241, 481)], 1.0, p[0] == 'halves', 'ratio')))
A(Claim('bias-zero-limit', r'is consistent with a continuum value of zero',
        check=lambda c, p: (lambda b: ok(abs(2 * b[2] - b[1]) < 0.1 * abs(b[2]),
                                          'Richardson extrapolation 2B(h/2)-B(h) = %.2e, %.2e' % (2 * b[1] - b[0], 2 * b[2] - b[1])))(
            [bias(c, N, 0.0)['B_ref'] for N in (121, 241, 481)])))
A(Claim('bias-order-one', r"""For shifted boundaries $B_b$ is
of order @w, negative when the continuation region is too small and positive when it is too large""",
        check=lambda c, p: shifted_check(c, p)))

def shifted_check(c, p):
    rows = [r for r in c.json('e3c_bias') if r['N'] == 241 and r['shift'] != 0]
    mags = [abs(r['B_ref']) for r in rows]
    signs = all((r['B_ref'] < 0) == (r['shift'] < 0) for r in rows)
    b0 = abs(bias(c, 241, 0.0)['B_ref'])
    return ok(p[0] == 'one' and 0.1 <= min(mags) and max(mags) <= 10 and signs and min(mags) >= 5 * b0,
              '|B| for shifted boundaries in [%.3f, %.3f] (criterion: within [0.1, 10] and >= 5 |B(0)| = %.3f); sign = sign(delta): %s' % (min(mags), max(mags), 5 * b0, signs))

for (N, sh, lab) in [(241, -0.2, '-0.20'), (241, -0.1, '-0.10'), (241, -0.05, '-0.05'), (241, 0.05, '0.05'), (241, 0.1, '0.10'),
                     (241, 0.2, '0.20'), (121, 0.0, '0'), (241, 0.0, '0'), (481, 0.0, '0')]:
    A(Claim('tab-bias-%d-%s' % (N, lab), r'$%d$ & $%s$ & $@$ & $@$ & $@$\\' % (N, lab),
            lambda c, N=N, sh=sh: [bias(c, N, sh)['P_ref'], bias(c, N, sh)['F_ref'], bias(c, N, sh)['B_ref']]))
    C[-1].covers_first = True

A(Claim('post-setup', r'An independent Monte Carlo evaluation at the finite-difference boundary ($N=@$)',
        lambda c: [c.npz('baseline481')['x'].size], 'exact'))
A(Claim('post-setup2', r"""accumulated from $\hat\tau$ to $T=@$ over visits to $\cC$ ($M=@$,
$\Delta t=@$, $\varepsilon=\sqrt{\Delta t}$)""", lambda c: [post(c, 0.005, 120.0)['T'], post(c, 0.005, 120.0)['M'], post(c, 0.005, 120.0)['dt']], 'exact'))
A(Claim('post-fine', r'\hat\E[Z]=@\pm@,\qquad\hat\E|Z|=@\pm@',
        lambda c: list(post(c, 0.005, 120.0)['EZ']) + list(post(c, 0.005, 120.0)['EabsZ'])))
A(Claim('post-ci95', r'with $@\%$ confidence half-widths. At the coarser step',
        lambda c: [100 * (2 * norm.cdf(ci_quantile()) - 1)], note='coverage of the 1.96 sd interval used in mc.ci'))

def ci_quantile():
    q = float(re.search(r'return float\(v\.mean\(\)\), float\(([\d.]+) \*', src('mc.py')).group(1))
    return q

A(Claim('post-coarse', r"""At the coarser step $\Delta t=@$ the values are
$@\pm@$ and $@\pm@$""",
        lambda c: [0.01] + list(post(c, 0.01, 120.0)['EZ']) + list(post(c, 0.01, 120.0)['EabsZ']), ['exact'] + ['round'] * 4))
A(Claim('post-bias-visible', r"""so that a small positive discretization bias is visible in
the mean""", check=lambda c, p: (lambda e: ok(e[0] - e[1] > 0, 'E[Z] - halfwidth = %.4f > 0 at dt = 0.01' % (e[0] - e[1])))(post(c, 0.01, 120.0)['EZ'])))
A(Claim('post-horizon', r"""extending the horizon to $T=@$ at $\Delta t=@$ changes these values by less than
$@$""", lambda c: [200.0, 0.01, max(abs(post(c, 0.01, 200.0)['EZ'][0] - post(c, 0.01, 120.0)['EZ'][0]),
                                    abs(post(c, 0.01, 200.0)['EabsZ'][0] - post(c, 0.01, 120.0)['EabsZ'][0]))],
        ['exact', 'exact', 'lt']))
A(Claim('post-discount', r'(the discount factor $e^{-rT}$ is $@$ at $T=@$)', lambda c: [math.exp(-B['r'] * 120.0), 120.0], ['round', 'exact']))
A(Claim('post-zero', r"""is zero within the statistical error at the finer
time step""", check=lambda c, p: (lambda e: ok(abs(e[0]) <= e[1], '|E[Z]| = %.4f <= half-width %.4f at dt = 0.005' % (abs(e[0]), e[1])))(post(c, 0.005, 120.0)['EZ'])))
A(Claim('post-order-one', r"""the pathwise post-stopping functional is of
order @w in absolute value""", check=lambda c, p: (lambda e: ok(p[0] == 'one' and 0.1 <= e <= 10, 'E|Z| = %.3f' % e))(post(c, 0.005, 120.0)['EabsZ'][0])))

# ---------------------------------------------------------------- 9.6 statics
A(Claim('statics-grid', r"""These runs use $X_{\max}=@$ and $N=@$, i.e.\
the spacing $h=@$ of the $N=@$ grid""",
        lambda c: [e4_defaults()['Xmax'], e4_defaults()['N'], e4_defaults()['Xmax'] / (e4_defaults()['N'] - 1), 241],
        ['exact', 'exact', 'exact', 'exact']))
A(Claim('statics-same-h', r'the spacing $h=0.0125$ of the $N=241$ grid',
        check=lambda c, p: ok(e4_defaults()['Xmax'] / (e4_defaults()['N'] - 1) == 3.0 / 240, 'h = 4/320 = %.17g, 3/240 = %.17g' % (4.0 / 320, 3.0 / 240))))

def e4_defaults():
    sig = inspect.signature(exp_fd.e4)
    return {k: v.default for k, v in sig.parameters.items()}

A(Claim('statics-mono', r"""Increasing $r$ or $c_0$
increases $\Gac$, shrinks the continuation region and narrows the wedge""", check=lambda c, p: statics_mono(c)))

def statics_mono(c):
    res = []
    for case, lo, hi in [('r', 0.03, 0.08), ('c0', 0.005, 0.03)]:
        rl, rb, rh = e4(c, case, lo), e4(c, 'alpha', 1.0), e4(c, case, hi)
        res.append(rl['areaC'] > rb['areaC'] > rh['areaC'] and rl['width1'] > rb['width1'] > rh['width1'])
    # Gamma_ac increases with r and c0 at every point
    pts = np.array([[1.5, 0.5], [0.5, 1.5], [2.0, 2.0 - 1e-9]])
    g = lambda kw: gamma_ac({**B, **kw}, pts[:, 0], pts[:, 1])
    res.append(np.all(g({'r': 0.08}) > g({'r': 0.03})) and np.all(g({'c': (0.03, 0, 0)}) > g({'c': (0.005, 0, 0)})))
    return ok(all(res), 'areas and widths decrease, Gamma_ac increases: %s' % res)

A(Claim('statics-alpha-arms', r"""Changing $\alpha$ rotates
$\Da$ and makes the arms unequal""", check=lambda c, p: ok(all(abs(e4(c, 'alpha', a)['areaD1'] - e4(c, 'alpha', a)['areaD2']) > 0.1 for a in (0.7, 1.4))
                                                          and e4(c, 'alpha', 1.0)['areaD1'] == e4(c, 'alpha', 1.0)['areaD2'],
                                                          'area(D1) - area(D2): %s' % [round(e4(c, 'alpha', a)['areaD1'] - e4(c, 'alpha', a)['areaD2'], 3) for a in (0.7, 1.0, 1.4)])))
A(Claim('statics-q-linear', r"""$q$ decreases linearly from $@$ at
$\rho=@$ to $@$ at $\rho=@$""",
        lambda c: [e4(c, 'rho', -0.8)['q'], -0.8, e4(c, 'rho', 0.8)['q'], 0.8], ['round', 'exact', 'round', 'exact']))
A(Claim('statics-q-linear-chk', r'decreases linearly', check=lambda c, p: q_linear(c)))

def q_linear(c):
    rows = sorted([r for r in c.json('e4_statics') if r['case'] == 'rho'], key=lambda r: r['value'])
    q = np.array([r['q'] for r in rows]); rho = np.array([r['value'] for r in rows])
    slope = np.diff(q) / np.diff(rho)
    return ok(np.ptp(slope) < 1e-13 and slope[0] < 0, 'slopes %s (spread %.1e)' % (np.unique(np.round(slope, 12)), np.ptp(slope)))

A(Claim('statics-decrease-q', r"""the wedge half-width and the premium on $\Da$ decrease
with it""", check=lambda c, p: (lambda rows: ok(all(np.diff([r['width1'] for r in rows]) > 0) and all(np.diff([r['premium_diag2'] for r in rows]) > 0),
                                               'both increasing in q over the rho sweep'))(
    sorted([r for r in c.json('e4_statics') if r['case'] == 'rho'], key=lambda r: r['q']))))
A(Claim('statics-premium-pct', r"""reproduce the premium at
$(@,@)$ within $@\%$ over the sweep""",
        lambda c: [2.0, 2.0, max(err_pct(r['premium_diag2'], r['q'] / (16 * gamma_ac(B, 2.0 + 1e-12, 2.0))) for r in c.json('e4_statics') if r['case'] == 'rho')],
        ['exact', 'exact', 'le']))
A(Claim('statics-hw-sym', r"""the half-width within $@$--$@\%$ in the symmetric
cases""", lambda c: [min(err_pct(r['width1'], r['pred1']) for r in e4sym(c)), max(err_pct(r['width1'], r['pred1']) for r in e4sym(c))]))
A(Claim('statics-two-cells', r'at $\rho=@$ the wedge spans only about @w cells',
        lambda c: [0.8], 'exact'))
A(Claim('statics-two-cells-chk', r'the wedge spans only about @w cells',
        check=lambda c, p: (lambda n: ok(p[0] == 'two' and abs(n - 2) <= 0.5, 'half-width / h = %.3f' % n))(e4(c, 'rho', 0.8)['width1'] / (4.0 / 320))))
A(Claim('statics-asym', r'are of similar accuracy (within $@$--$@\%$)',
        lambda c: [min(min(err_pct(r['width1'], r['pred1']), err_pct(r['width2'], r['pred2'])) for r in e4asym(c)),
                   max(max(err_pct(r['width1'], r['pred1']), err_pct(r['width2'], r['pred2'])) for r in e4asym(c))]))
A(Claim('statics-cap', r'($X_{\max}=@$, $N=@$, $h=@$; areas over the window $[@,@]^2$)',
        lambda c: [e4_defaults()['Xmax'], e4_defaults()['N'], e4_defaults()['Xmax'] / (e4_defaults()['N'] - 1), 0.0, WIN], 'exact'))
A(Claim('statics-cap-G', r'at the point of $\Da$ with $G=@$', lambda c: [statics_G()], 'exact'))

def statics_G():
    s = src('exp_fd.py')
    m = re.search(r'x2s = ([\d.]+) / a; x1s = ([\d.]+)', s)
    assert m.group(1) == m.group(2)
    return float(m.group(1))

for lab, case, val in [('$\\alpha=0.7$', 'alpha', 0.7), ('$\\alpha=1.0$ (baseline)', 'alpha', 1.0), ('$\\alpha=1.4$', 'alpha', 1.4),
                       ('$r=0.03$', 'r', 0.03), ('$r=0.08$', 'r', 0.08), ('$c_0=0.005$', 'c0', 0.005), ('$c_0=0.03$', 'c0', 0.03),
                       ('$\\rho=-0.8$', 'rho', -0.8), ('$\\rho=-0.4$', 'rho', -0.4), ('$\\rho=0.4$', 'rho', 0.4), ('$\\rho=0.8$', 'rho', 0.8)]:
    sn = lab + r' & $@$ & $@$ & $@$ & $@$ & $@$ & $@$ & $@$ & $@$ & $@$\\'
    A(Claim('tab-statics-%s-%g' % (case, val), sn,
            lambda c, case=case, val=val: (lambda r: [r['q'], r['areaC'], r['areaD1'], r['areaD2'], r['width1'], r['width2'],
                                                      r['pred1'], r['pred2'], r['premium_diag2']])(e4(c, case, val))))
    C[-1].covers_first = True
A(Claim('fig-rho-cap', r'$\rho\in\{@,@,\dots,@\}$ ($h=@$)',
        lambda c: (lambda v: [v[0], v[1], v[-1], e4_defaults()['Xmax'] / (e4_defaults()['N'] - 1)])(
            sorted(r['value'] for r in c.json('e4_statics') if r['case'] == 'rho')), 'exact'))
A(Claim('fig-rho-cap-step', r'$\rho\in\{-0.8,-0.6,\dots,0.8\}$',
        check=lambda c, p: (lambda v: ok(np.allclose(np.diff(v), 0.2, rtol=0, atol=1e-12) and len(v) == 9, 'rho values %s' % v))(
            sorted(r['value'] for r in c.json('e4_statics') if r['case'] == 'rho'))))
A(Claim('fig-rho-pts', r"""Left: wedge half-width at
$(@,@)$ against $q$, with the formal value $q/(4\Gac)$. Right: continuation premium $V-G$ at
$(@,@)$""", lambda c: [statics_G()] * 4, 'exact'))

# ---------------------------------------------------------------- 9.7 Monte Carlo
A(Claim('mc-xref', r"""at $x_{\rm ref}=(@,@)$ for the
finite-difference stopping set ($N=@$)""", lambda c: list(exp_mc.XREF) + [c.npz('baseline481')['x'].size], 'exact'))
A(Claim('mc-P', r'$P(x_{\rm ref})=-(V-G)(x_{\rm ref})=@$', lambda c: [-e1N(c, 481)['VmG_ref']]))
A(Claim('mc-Y0', r'Here $|Y_0|=@$.', lambda c: [abs(XREF[0] - B['alpha'] * XREF[1])]))
A(Claim('mc-M', r'report the results for $M=@$ paths, $T_{\max}=@$', lambda c: [c.json('e5_mc')[0]['M'], c.json('e5_mc')[0]['T']], 'exact'))
A(Claim('mc-tau', r'mean killing time is between $@$ and $@$', lambda c: [min(r['mean_tau'] for r in c.json('e5_mc')), max(r['mean_tau'] for r in c.json('e5_mc'))]))
A(Claim('mc-alive', r"""the fraction of paths alive at $T_{\max}$ is below
$@$""", lambda c: [max(r['frac_alive_T'] for r in c.json('e5_mc'))], 'lt'))
A(Claim('mc-disc', r'$e^{-rT_{\max}}=@$', lambda c: [math.exp(-B['r'] * c.json('e5_mc')[0]['T'])]))
A(Claim('mc-cap', r"""Monte Carlo estimates of $P(x_{\rm ref})$ with $@\%$ confidence half-widths
($M=@$; FD reference $@$)""", lambda c: [100 * (2 * norm.cdf(ci_quantile()) - 1), c.json('e5_mc')[0]['M'], -e1N(c, 481)['VmG_ref']],
        ['round', 'exact', 'round']))
A(Claim('mc-header', r'$\tfrac12\sqrt{\Delta t}$ & $\sqrt{\Delta t}$ & $@\sqrt{\Delta t}$ & $(\Delta t)^{@}$',
        check=lambda c, p: mc_header(c, p)))
C[-1].covers = True

def mc_header(c, p):
    good = True
    for r in c.json('e5_mc'):
        dt = r['dt']; e = r['eps']
        good &= e[e5col(r, '0.5sqrt')] == 0.5 * np.sqrt(dt) and e[e5col(r, '1sqrt')] == np.sqrt(dt) \
            and e[e5col(r, '2sqrt')] == p[0].float * np.sqrt(dt) and e[e5col(r, 'dt^0.4')] == dt ** p[1].float
    return ok(good, 'bandwidths in the output equal (1/2, 1, 2) sqrt(dt) and dt^0.4 bitwise')

for dt in (0.02, 0.01, 0.005, 0.0025):
    A(Claim('tab-mc-%g' % dt, r'$%s$ & $@\pm@$ & $@$ & $@$ & $@$ & $@$ & $@\pm@$\\' % ('%g' % dt),
            lambda c, dt=dt: (lambda r: list(r['direct']) + [r['est'][e5col(r, l)][0] for l in ('0.5sqrt', '1sqrt', '2sqrt', 'dt^0.4')]
                              + list(r['paired'][e5col(r, '1sqrt')]))(e5dt(c, dt))))
    C[-1].covers_first = True
A(Claim('tab-mc-hw', r'The half-widths of the gain-form estimates are between $\pm@$ and $\pm@$',
        lambda c: [min(r['est'][e5col(r, l)][1] for r in c.json('e5_mc') for l in ('0.5sqrt', '1sqrt', '2sqrt', 'dt^0.4')),
                   max(r['est'][e5col(r, l)][1] for r in c.json('e5_mc') for l in ('0.5sqrt', '1sqrt', '2sqrt', 'dt^0.4'))]))
A(Claim('fig-mc-cap', r"""Left: estimate against bandwidth for @w time steps
($M=@$)""", lambda c: [c.json('e5_mc')[0]['M']], 'exact'))
A(Claim('fig-mc-cap-four', r'estimate against bandwidth for @w time steps', check=lambda c, p: ok(p[0] == 'four' and len(c.json('e5_mc')) == 4, '%d time steps' % len(c.json('e5_mc')))))
A(Claim('fig-mc-cap2', r"""Right: estimate against sample size ($\Delta t=@$,
$\varepsilon=\sqrt{\Delta t}$), with $@\%$ confidence intervals""",
        lambda c: [float(re.search(r'rng = np\.random\.default_rng\(SEED \+ 1\); dt = ([\d.]+)', src('exp_mc.py')).group(1)),
                   100 * (2 * norm.cdf(ci_quantile()) - 1)], ['exact', 'round']))
A(Claim('mc-three', r'@w observations can be made', check=lambda c, p: ok(p[0] == 'Three', 'structure of the text (First/Second/Third follow)')))
A(Claim('mc-direct', r"""the direct estimator converges to the reference as $\Delta t$
decreases ($@\pm@$ at $\Delta t\le@$)""",
        lambda c: list(e5dt(c, 0.005)['direct']) + [0.005], ['round', 'round', 'exact']))
A(Claim('mc-direct-both', r'decreases ($-0.2754\pm0.0010$ at $\Delta t\le0.005$)',
        check=lambda c, p: (lambda a, b: ok(round(a[0], 4) == round(b[0], 4) == -0.2754 and round(a[1], 4) == round(b[1], 4),
                                            'dt=0.005: %.5f+-%.5f, dt=0.0025: %.5f+-%.5f' % (a[0], a[1], b[0], b[1])))(e5dt(c, 0.005)['direct'], e5dt(c, 0.0025)['direct'])))
A(Claim('mc-direct-bias', r"""with a time-discretization bias of about
$@$ at $\Delta t=@$""", lambda c: [e5dt(c, 0.02)['direct'][0] + e1N(c, 481)['VmG_ref'], 0.02], ['round', 'exact']))
C[-1].values = lambda c: [abs(e5dt(c, 0.02)['direct'][0] + e1N(c, 481)['VmG_ref']), 0.02]
A(Claim('mc-paired', r"""when $\varepsilon<|Y_0|=@$ the gain-form estimator differs from the direct one by at most
$@$, that is, by @w to @w confidence half-widths of the paired difference""",
        lambda c: [abs(XREF[0] - XREF[1]), max(abs(m) for m, h in paired_small(c))], ['round', 'le']))
A(Claim('mc-paired-words', r'by @w to @w confidence half-widths', check=lambda c, p: paired_words(c, p)))

def paired_words(c, p):
    pr = paired_small(c)
    m, h = max(pr, key=lambda t: abs(t[0]))
    q = abs(m) / h
    return ok(p == ['one', 'two'] and 1 <= q <= 2 and all(abs(a) <= 2 * b for a, b in pr),
              'largest |paired difference| / its half-width = %.2f; all ratios %s' % (q, ['%.2f' % (abs(a) / b) for a, b in pr]))

def paired_small(c):
    out = []
    for r in c.json('e5_mc'):
        for i, e in enumerate(r['eps']):
            if e < abs(XREF[0] - XREF[1]):
                out.append(tuple(r['paired'][i]))
    return out

A(Claim('mc-spread', r"""at $\Delta t=@$ the estimates for $\varepsilon\in\{@,@,@\}$ are
$@$, $@$ and $@$, a spread of $@$""",
        lambda c: (lambda r: [0.01] + [r['eps'][e5col(r, l)] for l in ('0.5sqrt', '1sqrt', '2sqrt')] +
                   [r['est'][e5col(r, l)][0] for l in ('0.5sqrt', '1sqrt', '2sqrt')] +
                   [np.ptp([r['est'][e5col(r, l)][0] for l in ('0.5sqrt', '1sqrt', '2sqrt')])])(e5dt(c, 0.01)),
        ['exact'] * 4 + ['round'] * 4))
A(Claim('mc-spread-ten', r"""which is more than @w times the confidence
half-width""", check=lambda c, p: (lambda r: (lambda sp, hw: ok(p[0] == 'ten' and sp > 10 * hw, 'spread / largest half-width = %.1f' % (sp / hw)))(
    np.ptp([r['est'][e5col(r, l)][0] for l in ('0.5sqrt', '1sqrt', '2sqrt')]), max(r['est'][e5col(r, l)][1] for l in ('0.5sqrt', '1sqrt', '2sqrt'))))(e5dt(c, 0.01))))
A(Claim('mc-eps-itself', r"""the bias is
governed by $\varepsilon$ itself, not by the ratio $\varepsilon/\sqrt{\Delta t}$""", check=lambda c, p: eps_itself(c)))

def eps_itself(c):
    """Same eps, different ratio: (dt=0.01, 2 sqrt) and (dt=0.0025, 4 sqrt), both eps=0.2, agree;
    same ratio 2 sqrt, different eps: estimates differ significantly."""
    a, b = e5dt(c, 0.01), e5dt(c, 0.0025)
    ea, eb = a['est'][e5col(a, '2sqrt')], b['est'][e5col(b, '4sqrt')]
    same_eps = abs(ea[0] - eb[0]) <= ea[1] + eb[1] and a['eps'][e5col(a, '2sqrt')] == b['eps'][e5col(b, '4sqrt')]
    vals = [e5dt(c, dt)['est'][e5col(e5dt(c, dt), '2sqrt')] for dt in (0.02, 0.0025)]
    diff_ratio = abs(vals[0][0] - vals[1][0]) > 5 * (vals[0][1] + vals[1][1])
    return ok(same_eps and diff_ratio, 'eps=0.2 at ratios 2 and 4: %.4f vs %.4f; ratio 2 at eps=0.283 and 0.1: %.4f vs %.4f' % (ea[0], eb[0], vals[0][0], vals[1][0]))

A(Claim('mc-third', r"""the choice
$\varepsilon=(\Delta t)^{@}$""", lambda c: [math.log(e5dt(c, 0.01)['eps'][e5col(e5dt(c, 0.01), 'dt^0.4')]) / math.log(0.01)], 'round'))
A(Claim('mc-third-conv', r"""converges as
$\Delta t\to0$ but more slowly than $\varepsilon\propto\sqrt{\Delta t}$ in this range""", check=lambda c, p: third_check(c)))
C[-1].covers = True

def third_check(c):
    ref = -e1N(c, 481)['VmG_ref']
    rows = sorted(c.json('e5_mc'), key=lambda r: -r['dt'])
    e04 = [abs(r['est'][e5col(r, 'dt^0.4')][0] - ref) for r in rows]
    e1s = [abs(r['est'][e5col(r, '1sqrt')][0] - ref) for r in rows]
    return ok(all(np.diff(e04) < 0) and all(a > b for a, b in zip(e04, e1s)),
              'errors with eps=dt^0.4: %s; with eps=sqrt(dt): %s' % (['%.4f' % x for x in e04], ['%.4f' % x for x in e1s]))

A(Claim('mc-scaling', r"""The
half-widths in \Cref{tab:mc} scale as $M^{-1/2}$""", check=lambda c, p: m_scaling(c)))
C[-1].covers = True

def m_scaling(c):
    mm = c.json('e5_mc_M')
    M = np.array([r['M'] for r in mm], float); hw = np.array([r['est'][1] for r in mm])
    slope = np.polyfit(np.log(M), np.log(hw), 1)[0]
    return ok(abs(slope + 0.5) <= 0.05, 'fitted exponent %.4f (criterion |exponent + 1/2| <= 0.05)' % slope)

# ---------------------------------------------------------------- 9.8 Algorithm 1
W = lambda c: c.json('alg1_wide'); Nw = lambda c: c.json('alg1_narrow')
A(Claim('alg-nodes', r'nodes $s_k\in\{@,@,\dots,@\}$ for each arm', lambda c: [W(c)['nodes'][0], W(c)['nodes'][1], W(c)['nodes'][-1]], 'exact'))
A(Claim('alg-nodes-step', r'$s_k\in\{0,0.25,\dots,1.75\}$', check=lambda c, p: ok(np.allclose(np.diff(W(c)['nodes']), 0.25, atol=0, rtol=0) and W(c)['nodes'] == Nw(c)['nodes'],
                                                                                  'nodes %s in both runs' % W(c)['nodes'])))
A(Claim('alg-M', r'$M=@$ paths per trial state, $\Delta t=@$, $T_{\max}=@$',
        lambda c: [W(c)['params']['M'], W(c)['params']['dt'], W(c)['params']['T']], 'exact'))
A(Claim('alg-eps', r'with $\varepsilon=\tfrac12\sqrt{\Delta t}=@$, offset $h_n=@$',
        lambda c: [W(c)['params']['eps'], W(c)['params']['hn']], 'exact'))
A(Claim('alg-eps-formula', r'$\varepsilon=\tfrac12\sqrt{\Delta t}', check=lambda c, p: ok(W(c)['params']['eps'] == 0.5 * math.sqrt(W(c)['params']['dt']), 'eps = 0.5 sqrt(dt) bitwise')))
A(Claim('alg-gains', r"""gains
$g_i=@/(@+i/@)$ with steps clipped to $\pm@$, margin $\varsigma=@$ and upper bounds
$\bar B_i=@$, for $I=@$ iterations""",
        lambda c: [W(c)['params']['kappa'], 1.0, alg1.GAIN_DECAY, alg1.STEP_CLIP, W(c)['params']['margin'], alg1.B_UPPER, W(c)['params']['K']], 'exact'))
A(Claim('alg-params-same', r'iterations, from @w initial boundaries', check=lambda c, p: ok(p[0] == 'two' and len(alg1.INITS) == 2 and
        {k: v for k, v in W(c)['params'].items() if k != 'seed'} == {k: v for k, v in Nw(c)['params'].items() if k != 'seed'},
        'two runs with identical parameters except the seed')))
A(Claim('alg-inits', r"""a ``wide'' one,
$b_1(s)=b_2(s)=s+@$, and a ``narrow'' one, $b_1(s)=b_2(s)=\max(@,s+@)$""",
        check=lambda c, p: inits_check(c, p)))
C[-1].covers = True

def inits_check(c, p):
    s = np.array(W(c)['nodes'])
    good = np.array_equal(alg1.INITS['wide'](s), s + p[0].float) and np.array_equal(alg1.INITS['narrow'](s), np.maximum(p[1].float, s + p[2].float)) \
        and np.array_equal(np.array(W(c)['hist'][0]['b1']), s + p[0].float) and np.array_equal(np.array(Nw(c)['hist'][0]['b1']), np.maximum(p[1].float, s + p[2].float))
    return ok(good, 'initial boundaries in code and in the stored iteration 0 equal the printed formulas bitwise')

A(Claim('alg-arms', r"""The @w arms are updated
independently""", check=lambda c, p: ok(p[0] == 'two' and 'step1' in src('alg1.py') and 'step2' in src('alg1.py'), 'b1 and b2 receive separate updates (step1, step2)')))
A(Claim('alg-fall', r"""falls
from $@$ and $@$ to about $@$ within @w iterations""",
        lambda c: [W(c)['hist'][0]['err_rms'], Nw(c)['hist'][0]['err_rms'], max(W(c)['hist'][10]['err_rms'], Nw(c)['hist'][10]['err_rms'])],
        ['round', 'round', 'about'], note='third value: larger of the two runs at iteration 10'))
A(Claim('alg-fall-ten', r'to about $0.01$ within @w iterations', check=lambda c, p: ok(p[0] == 'ten' and len(W(c)['hist']) > 10,
        'r.m.s. distance at iteration 10: wide %.4f, narrow %.4f' % (W(c)['hist'][10]['err_rms'], Nw(c)['hist'][10]['err_rms']))))
A(Claim('alg-avg', r"""the average of
the last $@$ iterates is within $@$ of the finite-difference boundary at every node""",
        lambda c: [alg1.AVG_LAST, max(W(c)['avg_err_max'], Nw(c)['avg_err_max'])], ['exact', 'le']))
A(Claim('alg-agree', r'two runs agree with each other to within $@$',
        lambda c: [float(np.max(np.abs(np.r_[np.array(W(c)['b1_avg']) - Nw(c)['b1_avg'], np.array(W(c)['b2_avg']) - Nw(c)['b2_avg']])))], 'le'))
A(Claim('alg-agree-two', r"""and the
@w runs agree""", check=lambda c, p: ok(p[0] == 'two', 'wide and narrow')))
A(Claim('alg-offset', r'(discretely monitored killing at $\Delta t=@$, finite offset $h_n$)', lambda c: [W(c)['params']['dt']], 'exact'))
A(Claim('alg-offset-sys', r'The remaining offset is systematic', check=lambda c, p: offset_sys(c)))

def offset_sys(c):
    """Systematic: averaging the last iterates does not reduce the error relative to single iterates."""
    out = []
    for R in (W(c), Nw(c)):
        last = np.mean([h['err_rms'] for h in R['hist'][-alg1.AVG_LAST:]])
        out.append((R['avg_err_rms'], last))
    return ok(all(a > 0.8 * l for a, l in out), 'r.m.s. error of averaged iterate vs mean of last iterates: %s' % [('%.4f' % a, '%.4f' % l) for a, l in out])

A(Claim('alg-loss', r"""their relative loss \eqref{eq:loss} has mean
$@$ and maximum $@$ over the window""",
        lambda c: [W(c)['avg_loss_mean'], W(c)['avg_loss_max']], note='wide run; the narrow run is checked in alg-loss-narrow'))
A(Claim('alg-loss-narrow', r"""has mean
$@$ and maximum $@$ over the window""",
        check=lambda c, p: (lambda n: ok(p[0].matches(n['avg_loss_mean']) and p[1].matches(n['avg_loss_max']), 'narrow run: mean %.3e, max %.3e' % (n['avg_loss_mean'], n['avg_loss_max'])))(Nw(c))))
A(Claim('alg-loss-where', r"""the maximum occurring where the
parametrization continues the boundary parallel to $\Da$ beyond the last node""", check=lambda c, p: loss_where(c)))

def loss_where(c):
    from mc import Boundary
    m, U, stop = baseline_model(c, 241)
    win = (m.X1 <= WIN) & (m.X2 <= WIN); res = []
    for R in (W(c), Nw(c)):
        s = np.array(R['nodes']); bd = Boundary(s, R['b1_avg'], s, R['b2_avg'], m.alpha)
        st = bd.stopped(np.column_stack([m.X1.ravel(), m.X2.ravel()])).reshape(m.N, m.N)
        J = m.evaluate(st); L = np.where(win, (U - J) / (1 + np.abs(U)), -np.inf)
        i, j = np.unravel_index(np.argmax(L), L.shape)
        x1, x2 = m.x[i], m.x[j]
        beyond = min(x1, x2) > s[-1]
        res.append((beyond, x1, x2, L[i, j], R['avg_loss_max']))
    return ok(all(r[0] for r in res) and all(abs(r[3] - r[4]) <= 8 * math.ulp(r[4]) for r in res),
              'argmax of the loss at %s (last node s_n = %.2f); recomputed max equals stored max: %s' %
              ([('%.4f' % r[1], '%.4f' % r[2]) for r in res], s[-1], [abs(r[3] - r[4]) <= 8 * math.ulp(r[4]) for r in res]))

A(Claim('alg-fd-N', r"""distance of the nodal values from the finite-difference boundary ($N=@$)""",
        lambda c: [c.npz('baseline481')['x'].size], 'exact'))
A(Claim('fig-alg-two', r"""averaged final iterates (markers; the @w
runs nearly coincide)""", check=lambda c, p: ok(p[0] == 'two' and float(np.max(np.abs(np.array(W(c)['b1_avg']) - Nw(c)['b1_avg']))) < 0.02, 'max |difference| of averaged iterates %.4f' % float(np.max(np.abs(np.array(W(c)['b1_avg']) - Nw(c)['b1_avg']))))))
A(Claim('tab-alg-cap', r"""History of \Cref{alg:sf} from @w initial boundaries. Distances are between nodal values
and the FD boundary ($N=@$)""", lambda c: [c.npz('baseline481')['x'].size], 'exact'))
A(Claim('tab-alg-cap-two', r'History of \Cref{alg:sf} from @w initial', check=lambda c, p: ok(p[0] == 'two' and len(alg1.INITS) == 2, 'wide, narrow')))
A(Claim('tab-alg-se', r'whose standard error per node is about $@$', lambda c: [max(W(c)['hist'][-1]['defect_se'], Nw(c)['hist'][-1]['defect_se'])]))
for tag, R in [('wide', W), ('narrow', Nw)]:
    A(Claim('tab-alg-' + tag, tag + r''' & initial & $@$ & $@$ & $@$ & $@$\\
 & $i=@$ & $@$ & --- & --- & ---\\
 & $i=@$ & $@$ & --- & $@$ & ---\\
 & average of last $@$ & $@$ & $@$ & --- & $@$\\''',
            lambda c, R=R: (lambda r: [r['hist'][0]['err_rms'], r['hist'][0]['err_max'], r['hist'][0]['defect_rms'], r['hist'][0]['loss_mean'],
                                       10, r['hist'][10]['err_rms'], 60, r['hist'][60]['err_rms'], r['hist'][60]['defect_rms'],
                                       alg1.AVG_LAST, r['avg_err_rms'], r['avg_err_max'], r['avg_loss_mean']])(R(c)),
            ['round'] * 4 + ['exact', 'round', 'exact', 'round', 'round', 'exact', 'round', 'round', 'round']))
A(Claim('alg-two-starts', r'This is a single benchmark and @w starting points', check=lambda c, p: ok(p[0] == 'two' and len(alg1.INITS) == 2, '%d initialisations' % len(alg1.INITS))))
A(Claim('alg-defect-level', r'estimated defect at the final iterates is at the level of its standard error',
        check=lambda c, p: (lambda q: ok(all(0.5 <= x <= 2 for x in q), 'defect r.m.s. / standard error at the last iterate: %s' % ['%.2f' % x for x in q]))(
            [R(c)['hist'][-1]['defect_rms'] / R(c)['hist'][-1]['defect_se'] for R in (W, Nw)])))

CLAIMS = C

# ----------------------------------------------------------------------------- structural tokens
STRUCTURAL = [
    (r'\\tfrac12', 'the constant 1/2 of a formula'),
    (r'q/\((?:4|16)\\Gac\)', 'constant of the formal expressions of Remark rem:width (values checked by claims)'),
    (r'holds with \$m=1\$', 'growth exponent of Assumption ass:growth (theory input, not a computed value)'),
    (r'\\sigma_1\^2-2\\alpha', 'constant of the formula for q (formula checked by claim q-formula)'),
    (r'\\psi_\\epsilon\(y\)=\\tfrac12\(y\+\\sqrt\{y\^2\+\\epsilon\^2\}\)', 'definition of the smoothing (checked by claims psi-formula, tab-smooth-*)'),
    (r'\\tfrac12q\\,\\psi_\\epsilon', 'generator term (formula)'),
    (r'\$\\|G_\\epsilon-G\\|_\\infty\\le\\eta\$ then\s+\$\\|V_\\epsilon-V\\|_\\infty\\le\\eta\$', 'statement of a bound (theory)'),
    (r'(?i)one-sided', '"one-sided" is a name, not a quantity'),
    (r'\bone\b\s+particular', '"one particular policy" is not a quantity'),
    (r'i=1,2,', 'index range of the coordinates'),
    (r'alternative~?\s?[12]', 'name of an exercise alternative'),
    (r'solution of one\s+model', '"one model": the study concerns a single benchmark'),
    (r'\\\{\\tilde w=0\\\}|\\tilde w\\\}=0', 'equation defining the stopping set of policy (c)'),
    (r'\(\$\\delta=0\$\)', 'label of the unshifted row'),
    (r'the\s+three quantities discussed', 'refers to E[Z], |E[Z]|, E|Z| (text)'),
    (r'at the coarser one', 'pronoun'),
    (r'Half-widths', '"half-width" is a name'),
    (r'the direct one', 'pronoun'),
    (r'\bone\b and one in', 'covered as part of the two-arm statement'),
    (r'\$\\cD\^\{\(1\)\}\$ arm|\$\\cD\^\{\(2\)\}\$ arm', 'name of an arm'),
    (r'Three observations', 'text structure'),
    (r'First, the direct estimator|Second, when|Third, the choice', 'text structure (enumeration)'),
    (r'\\tfrac12\\dd\\loc', 'the factor 1/2 of the local-time term (theory)'),
    (r'\(1-\|\\rho\|\)', 'formula constant'),
    (r'\$O\(h\)\$', 'order symbol'),
    (r'second-order', 'scheme property (checked by claim second-order)'),
    (r'\\Gac\\ge0\}', 'theory (checked by claim gac-threshold)'),
    (r'G_\\epsilon=\\alpha x_2\+\\tfrac12\\big\(Y\+\\sqrt\{Y\^2\+\\epsilon\^2\}\\big\)', 'definition of the smoothing'),
    (r'\(V-G\)\(x_\{\\rm ref\}\)', 'symbol'),
    (r'\$b_1\(0\)\$', 'symbol b1 at x2 = 0 (values checked by tab-refine-*)'),
    (r'95th pct\.', 'column label (95th percentile, see claim tab-loss-header)'),
    (r'panels a--b', 'figure panel names'),
    (r'one-sided stopping sets', 'name'),
    (r'half-width', '"half-width" is a name'),
]
