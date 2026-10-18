"""One-dimensional closed-form diagnostic (Brownian motion, r = 1/2, c = 0, g(x) = |x|).
Checks: automatic killed trace, smooth-fit root, signed post-stopping bias, and the
deterministic smooth-fit iteration b <- b + kappa * P_b'(b-)."""
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad
from common import save

bstar = brentq(lambda b: b * np.tanh(b) - 1, 0.5, 3)
P = lambda b, x: abs(x) - b * np.cosh(x) / np.cosh(b)                  # killed potential on (-b, b)
dP = lambda b: 1 - b * np.tanh(b)                                       # P_b'(b-)
def F(b, x):                                                            # unrestricted potential of Gamma 1_(-b,b)
    ac = quad(lambda y: np.exp(-abs(x - y)) * 0.5 * abs(y), -b, b, points=[0.0, x] if abs(x) < b else [0.0])[0]
    return ac - np.exp(-abs(x))                                         # minus potential of delta_0 (density e^{-|x-y|})
rows = []
for b in [0.6, bstar, 2.0]:
    rows.append(dict(b=b, trace=P(b, b), dP=dP(b), killed0=P(b, 0.0), unres0=F(b, 0.0), bias0=F(b, 0.0) - P(b, 0.0),
                     bias_formula=np.exp(-b) * (b * np.tanh(b) - 1), F_at_b=F(b, b)))
    print(rows[-1])
grid = np.linspace(0.3, 2.4, 85)
curve = dict(b=grid.tolist(), bias0=[np.exp(-b) * (b * np.tanh(b) - 1) for b in grid], dP=[dP(b) for b in grid])
its = {}
for b0 in [0.4, 2.2]:
    b = b0; h = [b]
    for k in range(25):
        b = b + 0.8 * dP(b); h.append(b)
    its[str(b0)] = h
print('b*', bstar, 'contraction factor at b*: ', 1 - 0.8 * (np.tanh(bstar) + bstar / np.cosh(bstar) ** 2), its['0.4'][:6], its['2.2'][:6])
save('ex1d', dict(bstar=bstar, rows=rows, curve=curve, iterations=its, slope=float(np.tanh(bstar) + bstar / np.cosh(bstar) ** 2)))
