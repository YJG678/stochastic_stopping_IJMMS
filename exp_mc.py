"""Monte Carlo experiments E5 (estimator study) and the signed post-stopping functional."""
import numpy as np, sys, time, os
from fd import BASE
from common import *
from mc import *

XREF = (0.9, 1.0); SEED = 20261005

def fd_boundary():
    d = np.load(os.path.join(OUT, 'baseline481.npz'))
    x = d['x']; keep = x <= 2.75
    return Boundary(x[keep], d['b1'][keep], x[keep], d['b2'][keep]), d

def e5():
    bd, d = fd_boundary()
    G0 = max(XREF[0], XREF[1])
    rng = np.random.default_rng(SEED)
    rows = []
    M = 200000; T = 40.0
    for dt in [0.02, 0.01, 0.005, 0.0025]:
        mult = np.array([0.5, 1.0, 2.0, 4.0]); eps = np.concatenate([mult * np.sqrt(dt), [dt ** 0.4, dt ** (1 / 3)]])
        t0 = time.time(); s = simulate(XREF, bd, M, dt, T, eps, rng)
        direct = G0 - s['pay']
        row = dict(dt=dt, M=M, T=T, mean_tau=float(s['tau'].mean()), frac_alive_T=float((s['tau'] >= T).mean()),
                   direct=ci(direct), ac=ci(s['ac']), labels=['0.5sqrt', '1sqrt', '2sqrt', '4sqrt', 'dt^0.4', 'dt^1/3'], eps=eps.tolist(),
                   est=[ci(s['ac'] - 0.5 * s['lt'][:, i]) for i in range(eps.size)],
                   paired=[ci(s['ac'] - 0.5 * s['lt'][:, i] - direct) for i in range(eps.size)],
                   lt=[ci(s['lt'][:, i]) for i in range(eps.size)], secs=time.time() - t0)
        rows.append(row); print(row, flush=True)
    save('e5_mc', rows)
    # convergence in M at dt = 0.005, eps = sqrt(dt)
    rng = np.random.default_rng(SEED + 1); dt = 0.005
    s = simulate(XREF, bd, 200000, dt, T, [np.sqrt(dt)], rng)
    v = s['ac'] - 0.5 * s['lt'][:, 0]
    save('e5_mc_M', [dict(M=m, est=ci(v[:m])) for m in [1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000]])

def e5post():
    """Signed and absolute post-stopping functional at the FD boundary."""
    bd, d = fd_boundary(); rows = []
    for (dt, Tp, M) in [(0.01, 120.0, 20000), (0.005, 120.0, 20000), (0.01, 200.0, 20000)]:
        rng = np.random.default_rng(SEED + 2)
        t0 = time.time()
        s = simulate(XREF, bd, M, dt, Tp, [np.sqrt(dt)], rng, post_T=Tp)
        Z = s['post'][:, 0]
        rows.append(dict(dt=dt, T=Tp, M=M, EZ=ci(Z), EabsZ=ci(np.abs(Z)), sdZ=float(Z.std()), tail=float(np.exp(-BASE['r'] * Tp)), secs=time.time() - t0))
        print(rows[-1], flush=True)
    save('e5_post', rows)

if __name__ == '__main__':
    for f in sys.argv[1:]:
        t = time.time(); globals()[f](); print(f, 'done in %.1fs' % (time.time() - t), flush=True)
