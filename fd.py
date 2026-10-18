"""Finite-difference tools for the reflected max-payoff stopping problem.

State: normally reflected correlated OU diffusion on [0, Xmax]^2
    dX^i = kappa_i (theta_i - X^i) dt + sigma_i dW^i + dL^i,  d<W^1,W^2> = rho dt
Payoff G = max(x1, alpha x2), running cost c = c0 + c1 x1 + c2 x2, discount r.

Discretisation (monotone, M-matrix):
  * central drift differences wherever they preserve monotonicity, first-order
    upwind otherwise (drift='upwind' forces upwinding everywhere),
  * central second differences,
  * 7-point cross-derivative stencil chosen by the sign of rho,
  * normal reflection at x_i = 0 and at the artificial boundary x_i = Xmax
    imposed by mirror ghost nodes (outer = 'neumann'), or Dirichlet U = G at
    the artificial boundary (outer = 'dirichlet').
"""
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

BASE = dict(r=0.05, alpha=1.0, kappa=(0.4, 0.4), theta=(1.0, 1.0),
            sigma=(0.4, 0.4), rho=0.0, c=(0.01, 0.0, 0.0), Xmax=3.0)


class Model:
    def __init__(self, N=121, outer='neumann', drift='central', **kw):
        self.drift = drift
        p = dict(BASE); p.update(kw)
        self.p = p; self.N = N; self.outer = outer
        self.Xmax = p['Xmax']; self.h = self.Xmax / (N - 1)
        self.x = np.linspace(0.0, self.Xmax, N)
        self.X1, self.X2 = np.meshgrid(self.x, self.x, indexing='ij')
        self.r = p['r']; self.alpha = p['alpha']
        self.G = np.maximum(self.X1, self.alpha * self.X2)
        c0, c1, c2 = p['c']
        self.c = c0 + c1 * self.X1 + c2 * self.X2
        self.L = self._assemble()
        self.I = sp.identity(N * N, format='csr')
        # dirichlet nodes of the artificial boundary (only for outer='dirichlet')
        self.outer_mask = np.zeros((N, N), bool)
        if outer == 'dirichlet':
            self.outer_mask[-1, :] = True; self.outer_mask[:, -1] = True

    # ------------------------------------------------------------------
    def _assemble(self):
        N, h, p = self.N, self.h, self.p
        k1, k2 = p['kappa']; t1, t2 = p['theta']; s1, s2 = p['sigma']; rho = p['rho']
        b1 = k1 * (t1 - self.X1); b2 = k2 * (t2 - self.X2)
        a11, a22, a12 = s1 * s1, s2 * s2, rho * s1 * s2
        ii, jj = np.meshgrid(np.arange(N), np.arange(N), indexing='ij')
        rows, cols, vals = [], [], []

        def refl(k):
            k = np.abs(k)
            return np.where(k > N - 1, 2 * (N - 1) - k, k)

        def add(di, dj, w):
            w = np.broadcast_to(w, (N, N))
            rows.append((ii * N + jj).ravel())
            cols.append((refl(ii + di) * N + refl(jj + dj)).ravel())
            vals.append(w.ravel().astype(float))

        # diffusion (pure second differences, net of the cross stencil)
        d1 = (a11 - abs(a12)) / (2 * h * h); d2 = (a22 - abs(a12)) / (2 * h * h)
        assert d1 >= -1e-14 and d2 >= -1e-14, 'cross stencil not monotone'
        add(1, 0, d1); add(-1, 0, d1); add(0, 0, -2 * d1)
        add(0, 1, d2); add(0, -1, d2); add(0, 0, -2 * d2)
        if a12 != 0.0:
            s = 1 if a12 > 0 else -1
            w = abs(a12) / (2 * h * h)
            add(1, s, w); add(-1, -s, w); add(0, 0, -2 * w)
        # drift: central differences where they keep the scheme monotone
        # (|b_i| h <= a_ii - |a_12|), first-order upwind elsewhere
        cen1 = (np.abs(b1) * h <= 2 * d1 * h * h + 1e-14) & (self.drift == 'central')
        cen2 = (np.abs(b2) * h <= 2 * d2 * h * h + 1e-14) & (self.drift == 'central')
        self.frac_central = float(min(cen1.mean(), cen2.mean()))
        add(1, 0, np.where(cen1, b1 / (2 * h), np.maximum(b1, 0) / h))
        add(-1, 0, np.where(cen1, -b1 / (2 * h), np.maximum(-b1, 0) / h))
        add(0, 0, np.where(cen1, 0.0, -np.abs(b1) / h))
        add(0, 1, np.where(cen2, b2 / (2 * h), np.maximum(b2, 0) / h))
        add(0, -1, np.where(cen2, -b2 / (2 * h), np.maximum(-b2, 0) / h))
        add(0, 0, np.where(cen2, 0.0, -np.abs(b2) / h))
        L = sp.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))),
                          shape=(N * N, N * N))
        L.sum_duplicates()
        return L

    # ------------------------------------------------------------------
    def evaluate(self, stop, payoff=None, cost=None):
        """Value of the policy 'stop at first entry into the boolean mask stop'.
        Solves (r - L_h) J = -c on the complement, J = payoff on the mask."""
        G = self.G if payoff is None else payoff
        c = self.c if cost is None else cost
        stop = (stop | self.outer_mask).ravel()
        J = G.ravel().copy()
        cont = np.where(~stop)[0]
        if cont.size:
            A = (self.r * self.I - self.L).tocsr()
            Acc = A[cont][:, cont].tocsc()
            rhs = -c.ravel()[cont] - A[cont][:, np.where(stop)[0]] @ J[stop]
            J[cont] = spla.spsolve(Acc, rhs)
        return J.reshape(self.N, self.N)

    def solve(self, payoff=None, allowed=None, maxit=200, verbose=False):
        """Howard policy iteration for min{(r-L_h)U + c, U - payoff} = 0.
        allowed: boolean mask of nodes where stopping is permitted (default all)."""
        G = self.G if payoff is None else payoff
        N = self.N
        allowed = np.ones((N, N), bool) if allowed is None else allowed
        A = (self.r * self.I - self.L).tocsr()
        gain = (A @ G.ravel() + self.c.ravel()).reshape(N, N)   # discrete stopping gain
        stop = allowed & (gain >= 0)
        for it in range(maxit):
            U = self.evaluate(stop, payoff=G)
            res = (A @ U.ravel() + self.c.ravel()).reshape(N, N)
            # policy improvement: stop where the obstacle term is the smaller one
            new = allowed & ((U - G) <= res)
            new |= self.outer_mask
            if verbose:
                print(it, int((new != (stop | self.outer_mask)).sum()))
            if np.array_equal(new, stop | self.outer_mask):
                break
            stop = new
        return U, (stop | self.outer_mask), it + 1

    # ------------------------------------------------------------------
    def residuals(self, U, stop, payoff=None):
        """Discrete variational-inequality residuals of a candidate (U, stop)."""
        G = self.G if payoff is None else payoff
        A = (self.r * self.I - self.L).tocsr()
        res = (A @ U.ravel() + self.c.ravel()).reshape(self.N, self.N)
        free = ~self.outer_mask
        return dict(
            majorisation=float(np.max(np.maximum(G - U, 0)[free])),
            superharmonic=float(np.max(np.maximum(-res, 0)[free])),
            complementarity=float(np.max(np.abs(res * (U - G))[free])),
            continuation_eq=float(np.max(np.abs(res)[free & ~stop])) if (free & ~stop).any() else 0.0,
            contact=float(np.max(np.abs(U - G)[stop])),
        )

    def stopping_gain(self):
        A = (self.r * self.I - self.L).tocsr()
        return (A @ self.G.ravel() + self.c.ravel()).reshape(self.N, self.N)

    def interp(self, F, x1, x2):
        from scipy.interpolate import RegularGridInterpolator
        return float(RegularGridInterpolator((self.x, self.x), F)([[x1, x2]])[0])
