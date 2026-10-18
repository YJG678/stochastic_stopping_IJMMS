"""Shared helpers: sub-cell free-boundary reconstruction, windows, statistics."""
import numpy as np, json, os
from fd import Model, BASE

# Results directory; can be redirected (e.g. by the verifier) with the NUMERICS_RESULTS variable.
OUT = os.environ.get('NUMERICS_RESULTS',
                     os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results'))
os.makedirs(OUT, exist_ok=True)


def save(name, obj):
    with open(os.path.join(OUT, name + '.json'), 'w') as f:
        json.dump(obj, f, indent=1, default=lambda o: o.tolist() if hasattr(o, 'tolist') else float(o))


def load(name):
    with open(os.path.join(OUT, name + '.json')) as f:
        return json.load(f)


def arm_boundary(m, U, stop, arm=1, payoff=None):
    """Sub-cell reconstruction of the free boundary of one stopping arm.

    arm=1: returns b1(x2) on the grid of x2 (stopping set {x1 >= b1(x2)} in E1);
    arm=2: returns b2(x1) on the grid of x1 (stopping set {x2 >= b2(x1)} in E2).
    Near a smooth-fit boundary U-G ~ (kappa/2) dist^2, so sqrt(U-G) is linear
    in the distance; the zero of the linear extrapolant through the last two
    continuation nodes locates the boundary inside the cell."""
    G = m.G if payoff is None else payoff
    w = np.maximum(U - G, 0.0)
    N, h, x = m.N, m.h, m.x
    b = np.full(N, np.nan)
    for k in range(N):
        if arm == 1:
            line_stop = stop[:, k] & (m.X1[:, k] > m.alpha * m.X2[:, k]); line_w = w[:, k]
        else:
            line_stop = stop[k, :] & (m.X1[k, :] < m.alpha * m.X2[k, :]); line_w = w[k, :]
        if not line_stop.any():
            continue
        i = int(np.argmax(line_stop))
        if i < 2:
            b[k] = x[i]; continue
        s1, s2 = np.sqrt(line_w[i - 1]), np.sqrt(line_w[i - 2])
        frac = s1 / (s2 - s1) if s2 > s1 > 0 else 0.5
        b[k] = x[i - 1] + h * min(max(frac, 0.0), 2.0)
    return b


def gamma_ac(p, x1, x2):
    """Absolutely continuous stopping-gain density c + rG - b.grad G."""
    c0, c1, c2 = p['c']; a = p['alpha']
    k1, k2 = p['kappa']; t1, t2 = p['theta']
    G = np.maximum(x1, a * x2)
    drift = np.where(x1 > a * x2, k1 * (t1 - x1), a * k2 * (t2 - x2))
    return c0 + c1 * x1 + c2 * x2 + p['r'] * G - drift


def qval(p):
    s1, s2 = p['sigma']; a = p['alpha']
    return s1 * s1 - 2 * a * p['rho'] * s1 * s2 + a * a * s2 * s2


def stats(L, mask):
    v = L[mask]
    return dict(mean=float(v.mean()), p95=float(np.percentile(v, 95)), max=float(v.max()))
