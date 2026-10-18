"""Algorithm 1 (heuristic): smooth-fit boundary iteration with Monte Carlo killed potentials.

For every boundary node z the continuation-side derivative of the killed potential
P_b = R^{C_b} Gamma is estimated by a one-sided second-order difference that uses
P_b(z) = 0 (the automatic Dirichlet trace):
      d P_b(z-) ~ [ -4 P_b(z - h e) + P_b(z - 2 h e) ] / (2 h),
and the node is moved by  b <- b + kappa * dP,  with a decreasing gain kappa_k = kappa/(1+k/10),
followed by projection onto the admissible class (margin to the diagonal, upper bound)."""
import numpy as np, sys, time, os
from fd import Model, BASE
from common import *
from mc import *

STEP_CLIP = 0.1      # each nodal update is clipped to [-STEP_CLIP, STEP_CLIP]
B_UPPER = 3.5        # upper bound of the admissible box
GAIN_DECAY = 10.0    # g_i = kappa / (1 + i / GAIN_DECAY)
INITS = {'wide': lambda s: s + 0.9, 'narrow': lambda s: np.maximum(1.0, s + 0.2)}
SEEDS = {'wide': 11, 'narrow': 12}
NODES = np.arange(0.0, 1.75 + 1e-9, 0.25)
AVG_LAST = 15


def run(tag, init_margin, K=60, M=20000, dt=0.01, T=25.0, hn=0.05, kappa=0.3, margin=0.15, seed=1):
    p = BASE; a = p['alpha']; rng = np.random.default_rng(seed)
    s = NODES.copy(); n = s.size
    b1 = init_margin(s); b2 = init_margin(s)
    eps = 0.5 * np.sqrt(dt)
    ref = np.load(os.path.join(OUT, 'baseline481.npz'))
    b1_fd = np.interp(s, ref['x'], ref['b1']); b2_fd = np.interp(s, ref['x'], ref['b2'])
    m = Model(N=241); U, stop, _ = m.solve(); win = (m.X1 <= 2.5) & (m.X2 <= 2.5)
    def fd_loss(b1, b2):
        bd = Boundary(s, b1, s, b2, a)
        st = bd.stopped(np.column_stack([m.X1.ravel(), m.X2.ravel()])).reshape(m.N, m.N)
        J = m.evaluate(st); L = (U - J) / (1 + np.abs(U))
        return float(L[win].mean()), float(L[win].max())
    hist = []
    for k in range(K + 1):
        bd = Boundary(s, b1, s, b2, a)
        starts = np.concatenate([np.column_stack([b1 - hn, s]), np.column_stack([b1 - 2 * hn, s]),
                                 np.column_stack([s, b2 - hn]), np.column_stack([s, b2 - 2 * hn])])
        x0 = np.repeat(starts, M, axis=0)
        sim = simulate(x0, bd, x0.shape[0], dt, T, [eps], rng, chunk=x0.shape[0])
        Pp = (sim['ac'] - 0.5 * sim['lt'][:, 0]).reshape(4 * n, M)
        P = Pp.mean(1); se = Pp.std(1, ddof=1) / np.sqrt(M)
        d1 = (-4 * P[:n] + P[n:2 * n]) / (2 * hn); d2 = (-4 * P[2 * n:3 * n] + P[3 * n:]) / (2 * hn)
        se_d = float(np.sqrt(16 * se[:n] ** 2 + se[n:2 * n] ** 2).mean() / (2 * hn))
        lm, lx = fd_loss(b1, b2)
        hist.append(dict(k=k, b1=b1.tolist(), b2=b2.tolist(), d1=d1.tolist(), d2=d2.tolist(),
                         defect_rms=float(np.sqrt(np.mean(np.r_[d1, d2] ** 2))), defect_se=se_d,
                         err_rms=float(np.sqrt(np.mean(np.r_[b1 - b1_fd, b2 - b2_fd] ** 2))),
                         err_max=float(np.max(np.abs(np.r_[b1 - b1_fd, b2 - b2_fd]))), loss_mean=lm, loss_max=lx))
        print(tag, k, 'defect rms %.4f (se %.4f)  bdry err rms %.4f max %.4f  loss mean %.2e max %.2e' %
              (hist[-1]['defect_rms'], se_d, hist[-1]['err_rms'], hist[-1]['err_max'], lm, lx), flush=True)
        if k == K: break
        gk = kappa / (1.0 + k / GAIN_DECAY)            # decreasing (Robbins-Monro type) gain
        step1 = np.clip(gk * d1, -STEP_CLIP, STEP_CLIP); step2 = np.clip(gk * d2, -STEP_CLIP, STEP_CLIP)
        b1 = np.clip(b1 + step1, a * s + margin, B_UPPER); b2 = np.clip(b2 + step2, s / a + margin, B_UPPER)
    # averaged final iterate (last 15)
    b1bar = np.mean([h['b1'] for h in hist[-AVG_LAST:]], 0); b2bar = np.mean([h["b2"] for h in hist[-AVG_LAST:]], 0)
    lm, lx = fd_loss(b1bar, b2bar)
    out = dict(tag=tag, nodes=s.tolist(), b1_fd=b1_fd.tolist(), b2_fd=b2_fd.tolist(), hist=hist,
               b1_avg=b1bar.tolist(), b2_avg=b2bar.tolist(), avg_err_rms=float(np.sqrt(np.mean(np.r_[b1bar - b1_fd, b2bar - b2_fd] ** 2))),
               avg_err_max=float(np.max(np.abs(np.r_[b1bar - b1_fd, b2bar - b2_fd]))), avg_loss_mean=lm, avg_loss_max=lx,
               params=dict(K=K, M=M, dt=dt, T=T, hn=hn, kappa=kappa, margin=margin, eps=eps, seed=seed))
    print(tag, 'AVERAGED: err rms %.4f max %.4f loss mean %.2e max %.2e' % (out['avg_err_rms'], out['avg_err_max'], lm, lx))
    save('alg1_' + tag, out)

if __name__ == '__main__':
    if sys.argv[1] == 'wide':
        run('wide', INITS['wide'], seed=SEEDS['wide'])
    else:
        run('narrow', INITS['narrow'], seed=SEEDS['narrow'])
