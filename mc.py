"""Monte Carlo tools: projected-Euler reflected OU paths, grid-detected killing,
band (occupation) estimator of the diagonal local time."""
import numpy as np
from fd import BASE
from common import gamma_ac, qval


class Boundary:
    """Two-sided candidate stopping set with piecewise-linear graphs
    D1 = {x1 >= b1(x2), x1 > a x2},  D2 = {x2 >= b2(x1), x1 < a x2}.
    Beyond the last node the graph is continued parallel to the diagonal."""
    def __init__(self, s1, b1, s2, b2, alpha=1.0):
        self.s1, self.b1, self.s2, self.b2, self.a = map(np.asarray, (s1, b1, s2, b2, alpha))
        self.a = float(alpha)

    def f1(self, x2):
        v = np.interp(x2, self.s1, self.b1)
        ex = x2 > self.s1[-1]
        return np.where(ex, self.b1[-1] + self.a * (x2 - self.s1[-1]), v)

    def f2(self, x1):
        v = np.interp(x1, self.s2, self.b2)
        ex = x1 > self.s2[-1]
        return np.where(ex, self.b2[-1] + (x1 - self.s2[-1]) / self.a, v)

    def stopped(self, X):
        x1, x2 = X[:, 0], X[:, 1]
        return ((x1 >= self.f1(x2)) & (x1 > self.a * x2)) | ((x2 >= self.f2(x1)) & (x1 < self.a * x2))


def simulate(x0, bd, M, dt, T, eps, rng, p=BASE, post_T=None, chunk=50000):
    """Returns per-path arrays:
       ac   = sum_{t_j < tau} e^{-r t_j} Gamma_ac(X_tj) dt
       lt   = sum_{t_j < tau} e^{-r t_j} (2 eps)^{-1} 1{|Y_tj| <= eps} q dt   (band estimate of int e^{-rs} dl^0_s)
       pay  = e^{-r tau} G(X_tau) - sum_{t_j<tau} e^{-r t_j} c(X_tj) dt       (realised policy payoff)
       tau  = grid-detected killing time (T if not killed)
       (x0 may also be an (M, 2) array of individual starting points)
       post = sum_{tau <= t_j < post_T} e^{-r t_j} 1_C(X_tj) dA^Gamma increment   (only if post_T is given)
    lt may be requested for several bandwidths at once (eps array)."""
    k = np.array(p['kappa']); th = np.array(p['theta']); sg = np.array(p['sigma']); rho = p['rho']; a = p['alpha']; r = p['r']
    c0, c1, c2 = p['c']; q = qval(p)
    eps = np.atleast_1d(np.asarray(eps, float))
    out = {key: [] for key in ['ac', 'lt', 'pay', 'tau', 'post']}
    horizon = T if post_T is None else post_T
    nsteps = int(round(horizon / dt)); sq = np.sqrt(dt)
    for start in range(0, M, chunk):
        m = min(chunk, M - start)
        x0a = np.asarray(x0, float)
        X = x0a[start:start + m].copy() if x0a.ndim == 2 else np.tile(x0a, (m, 1))
        alive = np.ones(m, bool); tau = np.full(m, float(T))
        ac = np.zeros(m); lt = np.zeros((m, eps.size)); cost = np.zeros(m); pay = np.zeros(m); post = np.zeros((m, eps.size))
        for j in range(nsteps + 1):
            t = j * dt; disc = np.exp(-r * t)
            act = alive if post_T is None else np.ones(m, bool)
            if not act.any(): break
            Xa = X[act]
            inD = bd.stopped(Xa)
            idx = np.where(act)[0]
            # killing (first entry, detected on the time grid) or horizon
            newly = idx[inD & alive[idx]] if t < T else idx[alive[idx]]
            if newly.size:
                Xn = X[newly]
                pay[newly] = disc * np.maximum(Xn[:, 0], a * Xn[:, 1]) - cost[newly]
                tau[newly] = t; alive[newly] = False
            if j == nsteps: break
            Y = Xa[:, 0] - a * Xa[:, 1]
            g = gamma_ac(p, Xa[:, 0], Xa[:, 1])
            band = (np.abs(Y)[:, None] <= eps[None, :]) * (q * dt / (2 * eps))[None, :]
            pre = alive[idx]
            ac[idx[pre]] += disc * g[pre] * dt
            lt[idx[pre]] += disc * band[pre]
            cost[idx[pre]] += disc * (c0 + c1 * Xa[pre, 0] + c2 * Xa[pre, 1]) * dt
            if post_T is not None:
                po = (~pre) & (~inD)                 # after tau, currently in the continuation set
                post[idx[po]] += disc * (g[po, None] * dt - 0.5 * band[po])
            # projected Euler step (normal reflection in the quadrant)
            Z = rng.standard_normal((idx.size, 2))
            if rho != 0.0:
                Z[:, 1] = rho * Z[:, 0] + np.sqrt(1 - rho * rho) * Z[:, 1]
            X[idx] = np.maximum(Xa + k * (th - Xa) * dt + sg * sq * Z, 0.0)
        out['ac'].append(ac); out['lt'].append(lt); out['pay'].append(pay); out['tau'].append(tau); out['post'].append(post)
    return {key: np.concatenate(v) for key, v in out.items()}


def ci(v):
    v = np.asarray(v, float)
    return float(v.mean()), float(1.96 * v.std(ddof=1) / np.sqrt(v.size))
