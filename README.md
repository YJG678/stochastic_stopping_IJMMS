# Code for "Singular Stopping Gains and Killed Resolvents for Reflected Diffusions with Max-Type Payoffs"

Python 3 with NumPy, SciPy and Matplotlib (tested with NumPy 2.5, SciPy 1.18, Matplotlib 3.11).
Run `./run_all.sh`; results are written to `results/` (JSON and NPZ) and figures to `../paper/figs/`.
The `results/` and `logs/` folders shipped here are the outputs used in the manuscript.

| File | Content |
|---|---|
| `fd.py` | Monotone finite-difference discretisation of the reflected OU generator; Howard policy iteration for the discrete obstacle problem; policy evaluation; discrete variational-inequality residuals. |
| `common.py` | Sub-cell free-boundary reconstruction, absolutely continuous gain `gamma_ac`, `qval`, statistics, I/O. |
| `exp_fd.py` | `e1` grid refinement and truncation study; `e2` consistency diagnostics; `e3` comparison policies and smoothing study; `e3c` killed vs unrestricted potentials for shifted boundaries; `e4` comparative statics. |
| `mc.py` | Projected-Euler simulation with grid-detected killing; band estimator of the local time; post-stopping functional. |
| `exp_mc.py` | `e5` estimator study at x_ref (time step and bandwidth); `e5post` signed and absolute post-stopping functional. |
| `alg1.py` | Algorithm 1 (heuristic smooth-fit boundary iteration), two initial boundaries. |
| `ex1d.py` | Closed-form one-dimensional example (killed trace, smooth-fit root, signed post-stopping term, exact iteration). |
| `figs.py` | All figures. |

## Model
Reflected correlated Ornstein-Uhlenbeck diffusion on the quadrant, payoff `G = max(x1, alpha*x2)`,
cost `c0 + c1*x1 + c2*x2`, discount `r`. Baseline parameters are in `fd.BASE`.

## Definitions of the comparison policies (`exp_fd.py: e3`)
* **one_retained**: stop on the `D^(2)` arm of the computed solution only (never stop where x1 > alpha*x2).
* **one_reopt**: solution of the discrete obstacle problem in which stopping is permitted only at nodes with x1 < alpha*x2.
* **no_singular**: stop on `{w = 0}`, where `w` solves `min{(r - L_h) w + Gamma_ac, w} = 0`, i.e. the gain-form
  problem with the local-time reward removed.
* **smoothing**: stopping set of the obstacle problem with payoff `alpha*x2 + (Y + sqrt(Y^2 + eps^2))/2`, `Y = x1 - alpha*x2`.
All policies are evaluated under the true payoff by the linear solve `Model.evaluate`.
Loss statistics use the nodes of the window `[0, 2.5]^2` with equal weights.

## Discretisation
* Mirror (Neumann) conditions at x_i = 0 and at the artificial boundary x_i = Xmax.
* Central drift differences where `|b_i| h <= a_ii - |a_12|`, upwind otherwise; 7-point cross-derivative stencil
  along the sign of `a_12` (requires `a_ii >= |a_12|`). The matrix `r I - L_h` is an M-matrix.
* Monte Carlo: `X <- max(X + b dt + sigma dW, 0)` componentwise; killing checked at grid times;
  `numpy.random.default_rng` (PCG64) with the seeds given in the scripts; 95% intervals are `1.96 * sd / sqrt(M)`.

## Verifying the numbers in the paper

`verify_numerics.py` checks every number and every number-based conclusion of the section
"Numerical study" against the code.

```
python3 verify_numerics.py SECTION.tex --mode quick   # re-runs the finite-difference experiments (~3 min)
python3 verify_numerics.py SECTION.tex --mode full    # re-runs everything, incl. Monte Carlo and Algorithm 1 (~1 h)
python3 verify_numerics.py SECTION.tex --mode stored  # checks the paper against the stored results only
python3 -m verify.selftest SECTION.tex                # negative controls: altered numbers must be detected
```

* **Re-execution.** Scripts are re-run into a fresh directory (`NUMERICS_RESULTS`), and every value is
  compared with `results/` in units in the last place; the default (`--max-ulp 0`) demands bitwise
  identity, which holds on the same platform because all randomness is seeded.
* **Printed numbers.** Each number is located by a verbatim quotation of the paper
  (`verify/claims_numerics.py`). A rounded number passes only if the exact binary value of the
  computed double, rounded half-up to the printed decimals or significant digits, *equals* the printed
  decimal (an exact test at the printed precision). Inputs of the code (parameters, grid sizes, seeds)
  must equal the configured doubles bitwise. Bounds are checked as inequalities.
* **Conclusions** ("halves with h", "two arms", "more than ten times", "decreases linearly", ...) are
  recomputed with the criterion stated in the report.
* **Coverage.** Every number token and number word of the section must be verified or explicitly
  classified as structural (subscript, formula constant, name), with the reason in the report.

The report (`verification_report.md` and `.json`) lists every check with the printed value, the code
value at full precision, the rule, the status and the source of the value (re-executed, stored, or
computed live). The exit status is 0 only if all checks pass, nothing is unaccounted for, and the
re-executed output is bitwise identical to the stored output.
