# Verification of the numerical section

- **section:** C:\Users\lenovo\Downloads\code\paper_section\section_numerics.tex
- **mode:** full
- **re-executed now:** ex1d.json, e1_refinement.json, baseline481.npz, e2_residuals.json, e3_policies.json, e3_maps.npz, e3c_bias.json, e4_statics.json, e5_mc.json, e5_mc_M.json, e5_post.json, alg1_wide.json, alg1_narrow.json
- **taken from stored output:** none
- **comparison rule:** printed decimals: exact binary value of the double rounded half-up to the printed precision must equal the printed decimal; inputs: bitwise equality
- **platform:** Windows-11-10.0.26200-SP0, Python 3.13.1, NumPy 2.4.4, SciPy 1.17.1
- **run time:** 4 s

## Summary

| | count |
|---|---|
| checks passed (exact at printed precision, bitwise for inputs, or conclusion holds) | 545 |
| approximate statements within one unit of the last printed digit | 1 |
| **checks failed** | **6** |
| number tokens in the section | 701 |
| ... verified by a check | 586 |
| ... structural (index, formula constant, label) | 115 |
| **... not accounted for** | **0** |

## Reproducibility of the code output (stored results vs. re-executed now)

| file | values compared | max ULP distance | bitwise identical |
|---|---|---|---|
| ex1d.json | 333 | 0 | yes |
| e1_refinement.json | 126 | 0 | yes |
| baseline481.npz | 464165 | 0 | yes |
| e2_residuals.json | 30 | 0 | yes |
| e3_policies.json | 84 | 0 | yes |
| e3_maps.npz | 522970 | 0 | yes |
| e3c_bias.json | 81 | 0 | yes |
| e4_statics.json | 176 | 0 | yes |
| e5_mc.json | 208 | 0 | yes |
| e5_mc_M.json | 24 | 0 | yes |
| e5_post.json | 30 | 0 | yes |
| alg1_wide.json | 2432 | 0 | yes |
| alg1_narrow.json | 2432 | 0 | yes |

## Failed checks

| line | claim | printed | code output (rounded as printed) | full value | rule | detail |
|---|---|---|---|---|---|---|
| 43 | param-seed | 20261005 |  |  | conclusion | seeds actually used: Sec. mcnum table 20261005, Fig. mc (M-sweep) 20261006, Sec. biasnum 20261007 |
| 82 | stable-digits | four |  |  | conclusion | values ['0.275289', '0.275211', '0.275187', '0.275182'] rounded to 4 significant digits give [0.2752, 0.2753] (N>=121 only: [0.2752]) |
| 108 | tab-refine-481 | 0.0063 | 0.0062 | 0.006249999999999645 | round |  |
| 148 | tab-res-superharmonic | 5\times10^{-13} | 4e-13 | 4.456521957019177e-13 | round |  |
| 149 | tab-res-complementarity | 5\times10^{-12} | 7e-12 | 6.870585194618192e-12 | round |  |
| 150 | tab-res-continuation_eq | 6\times10^{-13} | 5e-13 | 5.206859249318185e-13 | round |  |

## All checks

| line | claim | printed | code output (rounded as printed) | full value | rule | status | source | detail |
|---|---|---|---|---|---|---|---|---|
| 16 | kappa-positive | 0 | 0.4 | 0.4 | gt | PASS |  |  |
| 17 | rho-range | 1 | 0.8 | 0.8 | lt | PASS | fresh:e4_statics | largest \|rho\| used in any run |
| 19 | q-formula | (statement) |  |  | conclusion | PASS | fresh:e4_statics | q in the output equals the formula; dq/drho = -2 alpha s1 s2 = -0.32000000000000006 < 0 |
| 31 | param-r | 0.05 | 0.05 | 0.05 | exact | PASS |  |  |
| 32 | param-alpha | 1.0 | 1.0 | 1.0 | exact | PASS |  |  |
| 33 | param-kappa | 0.4 | 0.4 | 0.4 | exact | PASS |  |  |
| 33 | param-kappa | 0.4 | 0.4 | 0.4 | exact | PASS |  |  |
| 34 | param-theta | 1.0 | 1.0 | 1.0 | exact | PASS |  |  |
| 34 | param-theta | 1.0 | 1.0 | 1.0 | exact | PASS |  |  |
| 35 | param-sigma | 0.4 | 0.4 | 0.4 | exact | PASS |  |  |
| 35 | param-sigma | 0.4 | 0.4 | 0.4 | exact | PASS |  |  |
| 36 | param-rho | 0.0 | 0.0 | 0.0 | exact | PASS |  |  |
| 37 | param-c | 0.01 | 0.01 | 0.01 | exact | PASS |  |  |
| 37 | param-c | 0 | 0.0 | 0.0 | exact | PASS |  |  |
| 37 | param-c | 0 | 0.0 | 0.0 | exact | PASS |  |  |
| 39 | param-grid | 3 | 3.0 | 3.0 | exact | PASS | fresh:e1_refinement | Xmax values and N range of the refinement runs |
| 39 | param-grid | 4 | 4.0 | 4.0 | exact | PASS | fresh:e1_refinement | Xmax values and N range of the refinement runs |
| 39 | param-grid | 61 | 61.0 | 61.0 | exact | PASS | fresh:e1_refinement | Xmax values and N range of the refinement runs |
| 39 | param-grid | 481 | 481.0 | 481.0 | exact | PASS | fresh:e1_refinement | Xmax values and N range of the refinement runs |
| 39 | param-xmax-set | (statement) |  |  | conclusion | PASS | fresh:e1_refinement | Xmax in output: [3.0, 4.0] |
| 40 | param-window | 0 | 0.0 | 0.0 | exact | PASS |  |  |
| 40 | param-window | 2.5 | 2.5 | 2.5 | exact | PASS |  |  |
| 41 | param-xref | 0.9 | 0.9 | 0.9 | exact | PASS |  |  |
| 41 | param-xref | 1.0 | 1.0 | 1.0 | exact | PASS |  |  |
| 42 | param-mc | 0.0025 | 0.0025 | 0.0025 | exact | PASS | fresh:e5_mc |  |
| 42 | param-mc | 0.02 | 0.02 | 0.02 | exact | PASS | fresh:e5_mc |  |
| 42 | param-mc | 40 | 40.0 | 40.0 | exact | PASS | fresh:e5_mc |  |
| 42 | param-mc | 2\times10^5 | 200000.0 | 200000.0 | exact | PASS | fresh:e5_mc |  |
| 43 | param-seed | 20261005 |  |  | conclusion | FAIL |  | seeds actually used: Sec. mcnum table 20261005, Fig. mc (M-sweep) 20261006, Sec. biasnum 20261007 |
| 49 | central-drift | (statement) |  |  | conclusion | PASS | live:fd.Model assembly | fraction of nodes with central drift differences: [1.0, 1.0, 1.0, 1.0] |
| 49 | second-order | second |  |  | conclusion | PASS | live:fd.Model truncation test | interior truncation errors ['4.94e-04', '1.27e-04', '3.21e-05'], observed orders ['1.963', '1.982'] |
| 50 | monotone-correlated | 0 | 0.032 | 0.032 | gt | PASS | fresh:e4_statics |  |
| 51 | seven-point | seven |  |  | conclusion | PASS | live:fd.Model(rho=0.4) stencil | interior row of L_h for rho=0.4 has 7 nonzeros, off-diagonal min 5.69 |
| 51 | howard-iters | 15 | 15.0 | 15.0 | exact | PASS | fresh:e1_refinement |  |
| 51 | howard-iters | 28 | 28.0 | 28.0 | exact | PASS | fresh:e1_refinement |  |
| 51 | howard-iters | 54 | 54.0 | 54.0 | exact | PASS | fresh:e1_refinement |  |
| 51 | howard-iters | 107 | 107.0 | 107.0 | exact | PASS | fresh:e1_refinement |  |
| 51 | howard-iters | 61 | 61.0 | 61.0 | exact | PASS | fresh:e1_refinement |  |
| 51 | howard-iters | 121 | 121.0 | 121.0 | exact | PASS | fresh:e1_refinement |  |
| 51 | howard-iters | 241 | 241.0 | 241.0 | exact | PASS | fresh:e1_refinement |  |
| 51 | howard-iters | 481 | 481.0 | 481.0 | exact | PASS | fresh:e1_refinement |  |
| 54 | subcell-recon | two |  |  | conclusion | PASS | live:common.arm_boundary synthetic test | boundary recovered from two continuation nodes with error 4.44e-16 |
| 55 | area-weight | (statement) |  |  | conclusion | PASS | fresh:e4_statics,live:fd.Model(N=241).solve() | area(C) = #nodes x h^2 = 2.6592187500000004, stored 2.6592187500000004 |
| 55 | window-text | 0 | 0.0 | 0.0 | exact | PASS |  |  |
| 55 | window-text | 2.5 | 2.5 | 2.5 | exact | PASS |  |  |
| 62 | fig-N | 481 | 481.0 | 481.0 | exact | PASS | fresh:baseline481 |  |
| 62 | two-arms | two one one |  |  | conclusion | PASS | fresh:baseline481 | 2 connected components in the window, in ['E1', 'E2'] (on the full grid: 1, joined at the artificial corner) |
| 63 | narrows | (statement) |  |  | conclusion | PASS | fresh:baseline481 | half-width 1.463 at x2=0 -> 0.105 at x2=2.5; largest local increase 1.5e-03 <= h/2 = 3.1e-03 (sub-cell reconstruction staircase); no diagonal node stopped in (0,2.5]: True |
| 68 | gac-threshold | 0 | 0.26812500000000006 | 0.26812500000000006 | ge | PASS | fresh:baseline481 | first value: min of Gamma_ac over computed D1 (N=481) |
| 68 | gac-threshold | 0.867 | 0.867 | 0.8666666666666667 | round | PASS | fresh:baseline481 | first value: min of Gamma_ac over computed D1 (N=481) |
| 69 | arm-location | 1.46 | 1.4625000000000001 | 1.4625000000000001 | ge | PASS | fresh:baseline481 |  |
| 75 | fig-regions-N | 481 | 481.0 | 481.0 | exact | PASS | fresh:baseline481 |  |
| 76 | fig-regions-gac0 | 0 | 0 | 1.3877787807814457e-17 | round | PASS |  | \|Gamma_ac\| on E1 at the plotted line x1 = (kappa theta - c0)/(r + kappa) (figs.regions) |
| 82 | stable-digits | four |  |  | conclusion | FAIL | fresh:e1_refinement | values ['0.275289', '0.275211', '0.275187', '0.275182'] rounded to 4 significant digits give [0.2752, 0.2753] (N>=121 only: [0.2752]) |
| 83 | bdry-within | 0.01 | 0.008811226660491167 | 0.008811226660491167 | le | PASS | fresh:e1_refinement | largest spread over N of b1(0) and of the half-widths at 1.5, 2.0, 2.5 |
| 83 | truncation | 3 | 3.0 | 3.0 | exact | PASS |  |  |
| 83 | truncation | 4 | 4.0 | 4.0 | exact | PASS |  |  |
| 84 | truncation-check | (statement) |  |  | conclusion | PASS | fresh:e1_refinement | identical at the printed precision; max \|difference\| between X_max=3 and X_max=4 at equal h: 1.25e-10 |
| 84 | min-dist-equals-h | (statement) |  |  | conclusion | PASS | fresh:e1_refinement | max \|distance - h\| = 3.56e-16 <= 4 ulp(X_max) = 3.55e-15: equal to machine precision of the grid coordinates |
| 85 | min-dist-outer | (statement) |  |  | conclusion | PASS | fresh:e1_refinement | attained at x2 = [2.95, 2.975, 2.9875, 2.9938, 3.3, 3.975, 3.9875] |
| 86 | hw-text | 0.55 | 0.55 | 0.5503123874534122 | round | PASS | fresh:e1_refinement |  |
| 86 | hw-text | 1 | 1.0 | 1.0 | exact | PASS | fresh:e1_refinement |  |
| 86 | hw-text | 0.105 | 0.105 | 0.10513076870106808 | round | PASS | fresh:e1_refinement |  |
| 86 | hw-text | 2.5 | 2.5 | 2.5 | exact | PASS | fresh:e1_refinement |  |
| 87 | hw-formal-pct | 3 | 3 | 3.4111062558345617 | round | PASS | fresh:e1_refinement | N=481, x2 in {1.5, 2.0, 2.5} |
| 87 | hw-formal-pct | 11 | 11 | 11.073908223560359 | round | PASS | fresh:e1_refinement | N=481, x2 in {1.5, 2.0, 2.5} |
| 87 | hw-formal-pct | 1.5 | 1.5 | 1.5 | exact | PASS | fresh:e1_refinement | N=481, x2 in {1.5, 2.0, 2.5} |
| 87 | premium-25 | 2.5 | 2.5 | 2.5 | exact | PASS | fresh:baseline481 |  |
| 87 | premium-25 | 2.5 | 2.5 | 2.5 | exact | PASS | fresh:baseline481 |  |
| 87 | premium-25 | 0.0274 | 0.0274 | 0.02735581052046232 | round | PASS | fresh:baseline481 |  |
| 87 | premium-25 | 0.0272 | 0.0272 | 0.027210884353724835 | round | PASS | fresh:baseline481 |  |
| 90 | strict-cont | (statement) |  |  | conclusion | PASS | fresh:e2_residuals | min of V-G on the diagonal nodes in (0,2.5]: 0.02736 > 0, decreasing to the end of the window |
| 96 | tab-refine-cap | 3 | 3.0 | 3.0 | exact | PASS | fresh:e1_refinement |  |
| 96 | tab-refine-cap | 4 | 4.0 | 4.0 | exact | PASS | fresh:e1_refinement |  |
| 96 | tab-refine-cap | 0.0125 | 0.0125 | 0.0125 | exact | PASS | fresh:e1_refinement |  |
| 97 | tab-refine-cap-agree | (statement) |  |  | conclusion | PASS | fresh:e1_refinement | identical at the printed precision; max \|difference\| between X_max=3 and X_max=4 at equal h: 1.25e-10 |
| 103 | tab-refine-header | 1.5 | 1.5 | 1.5 | exact | PASS | fresh:e1_refinement |  |
| 103 | tab-refine-header | 2.0 | 2.0 | 2.0 | exact | PASS | fresh:e1_refinement |  |
| 103 | tab-refine-header | 2.5 | 2.5 | 2.5 | exact | PASS | fresh:e1_refinement |  |
| 105 | tab-refine-61 | 0.05 | 0.05 | 0.05 | exact | PASS | fresh:e1_refinement |  |
| 105 | tab-refine-61 | 0.27529 | 0.27529 | 0.2752892422448141 | round | PASS | fresh:e1_refinement |  |
| 105 | tab-refine-61 | 1.466 | 1.466 | 1.4656943807658709 | round | PASS | fresh:e1_refinement |  |
| 105 | tab-refine-61 | 0.249 | 0.249 | 0.24890705488152665 | round | PASS | fresh:e1_refinement |  |
| 105 | tab-refine-61 | 0.148 | 0.148 | 0.14795467893824554 | round | PASS | fresh:e1_refinement |  |
| 105 | tab-refine-61 | 0.106 | 0.106 | 0.10569195015967292 | round | PASS | fresh:e1_refinement |  |
| 105 | tab-refine-61 | 0.0500 | 0.0500 | 0.04999999999999982 | round | PASS | fresh:e1_refinement |  |
| 106 | tab-refine-121 | 0.025 | 0.025 | 0.025 | exact | PASS | fresh:e1_refinement |  |
| 106 | tab-refine-121 | 0.27521 | 0.27521 | 0.27521131228517404 | round | PASS | fresh:e1_refinement |  |
| 106 | tab-refine-121 | 1.457 | 1.457 | 1.4568831541053797 | round | PASS | fresh:e1_refinement |  |
| 106 | tab-refine-121 | 0.249 | 0.249 | 0.24905472429500985 | round | PASS | fresh:e1_refinement |  |
| 106 | tab-refine-121 | 0.147 | 0.147 | 0.14703967906916393 | round | PASS | fresh:e1_refinement |  |
| 106 | tab-refine-121 | 0.105 | 0.105 | 0.10464476498618502 | round | PASS | fresh:e1_refinement |  |
| 106 | tab-refine-121 | 0.0250 | 0.0250 | 0.02499999999999991 | round | PASS | fresh:e1_refinement |  |
| 107 | tab-refine-241 | 0.0125 | 0.0125 | 0.0125 | exact | PASS | fresh:e1_refinement |  |
| 107 | tab-refine-241 | 0.27519 | 0.27519 | 0.2751869254730297 | round | PASS | fresh:e1_refinement |  |
| 107 | tab-refine-241 | 1.463 | 1.463 | 1.4634883277506385 | round | PASS | fresh:e1_refinement |  |
| 107 | tab-refine-241 | 0.249 | 0.249 | 0.24937384995390555 | round | PASS | fresh:e1_refinement |  |
| 107 | tab-refine-241 | 0.147 | 0.147 | 0.14667704846628116 | round | PASS | fresh:e1_refinement |  |
| 107 | tab-refine-241 | 0.104 | 0.104 | 0.1041251682558646 | round | PASS | fresh:e1_refinement |  |
| 107 | tab-refine-241 | 0.0125 | 0.0125 | 0.012499999999999734 | round | PASS | fresh:e1_refinement |  |
| 108 | tab-refine-481 | 0.00625 | 0.00625 | 0.00625 | exact | PASS | fresh:e1_refinement |  |
| 108 | tab-refine-481 | 0.27518 | 0.27518 | 0.27518152758742787 | round | PASS | fresh:e1_refinement |  |
| 108 | tab-refine-481 | 1.463 | 1.463 | 1.463293880200727 | round | PASS | fresh:e1_refinement |  |
| 108 | tab-refine-481 | 0.250 | 0.250 | 0.2496170997229452 | round | PASS | fresh:e1_refinement |  |
| 108 | tab-refine-481 | 0.146 | 0.146 | 0.14593568077119823 | round | PASS | fresh:e1_refinement |  |
| 108 | tab-refine-481 | 0.105 | 0.105 | 0.10513076870106808 | round | PASS | fresh:e1_refinement |  |
| 108 | tab-refine-481 | 0.0063 | 0.0062 | 0.006249999999999645 | round | FAIL | fresh:e1_refinement |  |
| 110 | tab-refine-formal | 0.281 | 0.281 | 0.2807017543855217 | round | PASS |  |  |
| 110 | tab-refine-formal | 0.157 | 0.157 | 0.1568627450979008 | round | PASS |  |  |
| 110 | tab-refine-formal | 0.109 | 0.109 | 0.10884353741489934 | round | PASS |  |  |
| 120 | fig-refine-grids | three |  |  | conclusion | PASS |  | figs.refine plots N = 121, 241, 481 |
| 122 | fig-refine-cell | 0 2.5 one |  |  | conclusion | PASS | fresh:e1_refinement | nodal distance = h; reconstructed distance in the window [0.1057, 0.1017, 0.1017, 0.1051] (N >= 121 spread <= 0.005: resolved) |
| 131 | roundoff | (statement) |  |  | conclusion | PASS | fresh:e2_residuals | largest residual 1.25e-11 |
| 132 | sf-halves | halves |  |  | conclusion | PASS | fresh:e2_residuals | successive ratios ['1.848', '2.096'], observed orders ['0.886', '1.067'] (criterion: \|order - 1\| <= 0.25) |
| 133 | neumann-order | second |  |  | conclusion | PASS | fresh:e2_residuals | successive ratios ['3.827', '3.911'], observed orders ['1.936', '1.967'] (criterion: \|order - 2\| <= 0.25) |
| 140 | tab-res-four | first four |  |  | conclusion | PASS | fresh:e2_residuals | rows: majorization, superharmonicity, complementarity, continuation equation |
| 145 | tab-res-header | 121 | 121.0 | 121.0 | exact | PASS | fresh:e2_residuals |  |
| 145 | tab-res-header | 241 | 241.0 | 241.0 | exact | PASS | fresh:e2_residuals |  |
| 145 | tab-res-header | 481 | 481.0 | 481.0 | exact | PASS | fresh:e2_residuals |  |
| 147 | tab-res-majorisation | 0 | 0 | 0.0 | round | PASS | fresh:e2_residuals |  |
| 147 | tab-res-majorisation | 0 | 0 | 0.0 | round | PASS | fresh:e2_residuals |  |
| 147 | tab-res-majorisation | 0 | 0 | 0.0 | round | PASS | fresh:e2_residuals |  |
| 148 | tab-res-superharmonic | 5\times10^{-13} | 4e-13 | 4.456521957019177e-13 | round | FAIL | fresh:e2_residuals |  |
| 148 | tab-res-superharmonic | 3\times10^{-12} | 3e-12 | 2.9467626255774704e-12 | round | PASS | fresh:e2_residuals |  |
| 148 | tab-res-superharmonic | 1\times10^{-11} | 1e-11 | 1.1132214941533825e-11 | round | PASS | fresh:e2_residuals |  |
| 149 | tab-res-complementarity | 3\times10^{-13} | 3e-13 | 2.566667150366695e-13 | round | PASS | fresh:e2_residuals |  |
| 149 | tab-res-complementarity | 1\times10^{-12} | 1e-12 | 1.2452966934226445e-12 | round | PASS | fresh:e2_residuals |  |
| 149 | tab-res-complementarity | 5\times10^{-12} | 7e-12 | 6.870585194618192e-12 | round | FAIL | fresh:e2_residuals |  |
| 150 | tab-res-continuation_eq | 6\times10^{-13} | 5e-13 | 5.206859249318185e-13 | round | FAIL | fresh:e2_residuals |  |
| 150 | tab-res-continuation_eq | 3\times10^{-12} | 3e-12 | 2.9467626255774704e-12 | round | PASS | fresh:e2_residuals |  |
| 150 | tab-res-continuation_eq | 1\times10^{-11} | 1e-11 | 1.251464730456231e-11 | round | PASS | fresh:e2_residuals |  |
| 151 | tab-res-smoothfit_max | 0.110 | 0.110 | 0.10982011805866776 | round | PASS | fresh:e2_residuals |  |
| 151 | tab-res-smoothfit_max | 0.059 | 0.059 | 0.05942222206183345 | round | PASS | fresh:e2_residuals |  |
| 151 | tab-res-smoothfit_max | 0.028 | 0.028 | 0.02835556260663452 | round | PASS | fresh:e2_residuals |  |
| 152 | tab-res-neumann | 5.8\times10^{-4} | 5.8e-4 | 0.0005770169552166138 | round | PASS | fresh:e2_residuals |  |
| 152 | tab-res-neumann | 1.5\times10^{-4} | 1.5e-4 | 0.0001507574772308118 | round | PASS | fresh:e2_residuals |  |
| 152 | tab-res-neumann | 3.9\times10^{-5} | 3.9e-5 | 3.854935783920155e-05 | round | PASS | fresh:e2_residuals |  |
| 161 | pol-N | 241 | 241.0 | 241.0 | exact | PASS | fresh:e3_policies |  |
| 163 | pol-meanV | 1.769 | 1.769 | 1.7685410743837457 | round | PASS | fresh:e3_policies |  |
| 169 | pol-epigraph | (statement) |  |  | conclusion | PASS | fresh:e3_policies | every column of the stopping mask is monotone in x2 |
| 170 | pol-firstrow | 1.4 | 1.3250000000000002 | 1.3250000000000002 | le | PASS | fresh:e3_maps | onset: smallest x1 from which the re-optimised stopping set starts at the first node above the diagonal; the property must hold for all x1 >= printed value |
| 170 | pol-firstrow-word | first |  |  | conclusion | PASS | fresh:e3_maps | gap = h from x1 = 1.3250 on |
| 172 | pol-ab-means | 11.7 | 11.7 | 11.679342304609735 | round | PASS | fresh:e3_policies |  |
| 172 | pol-ab-means | 13.6 | 13.6 | 13.611494379903377 | round | PASS | fresh:e3_policies |  |
| 172 | pol-ab-order | (statement) |  |  | conclusion | PASS | fresh:e3_policies | ratio of means 0.858 |
| 173 | pol-ab-concentrated | (statement) |  |  | conclusion | PASS | fresh:e3_maps | one_retained: 69% of the loss in 29% of the window; one_reopt: 74% of the loss in 29% of the window (region: computed D1) |
| 175 | pol-onesided-consistent | (statement) |  |  | conclusion | PASS |  | statement about the theory; no number |
| 181 | tab-loss-cap | 0 | 0.0 | 0.0 | exact | PASS | fresh:e3_policies |  |
| 181 | tab-loss-cap | 2.5 | 2.5 | 2.5 | exact | PASS | fresh:e3_policies |  |
| 181 | tab-loss-cap | 241 | 241.0 | 241.0 | exact | PASS | fresh:e3_policies |  |
| 188 | tab-loss-header | (statement) |  |  | conclusion | PASS |  | 95th percentile computed with numpy.percentile(.., 95) in common.stats |
| 190 | tab-loss-one_retained | 13.61 | 13.61 | 13.611494379903377 | round | PASS | fresh:e3_policies |  |
| 190 | tab-loss-one_retained | 40.91 | 40.91 | 40.91180019810252 | round | PASS | fresh:e3_policies |  |
| 190 | tab-loss-one_retained | 47.10 | 47.10 | 47.101525729381 | round | PASS | fresh:e3_policies |  |
| 190 | tab-loss-one_retained | 0.390 | 0.390 | 0.39035445446579836 | round | PASS | fresh:e3_policies |  |
| 190 | tab-loss-one_retained | 1.345 | 1.345 | 1.3451845253044425 | round | PASS | fresh:e3_policies |  |
| 190 | tab-loss-one_retained | 1.649 | 1.649 | 1.648553400528335 | round | PASS | fresh:e3_policies |  |
| 191 | tab-loss-one_reopt | 11.68 | 11.68 | 11.679342304609735 | round | PASS | fresh:e3_policies |  |
| 191 | tab-loss-one_reopt | 38.65 | 38.65 | 38.65376034617565 | round | PASS | fresh:e3_policies |  |
| 191 | tab-loss-one_reopt | 45.30 | 45.30 | 45.296737159571016 | round | PASS | fresh:e3_policies |  |
| 191 | tab-loss-one_reopt | 0.338 | 0.338 | 0.33802630684335855 | round | PASS | fresh:e3_policies |  |
| 191 | tab-loss-one_reopt | 1.268 | 1.268 | 1.267932871355332 | round | PASS | fresh:e3_policies |  |
| 191 | tab-loss-one_reopt | 1.585 | 1.585 | 1.5853858005849855 | round | PASS | fresh:e3_policies |  |
| 192 | tab-loss-no_singular | 1.91 | 1.91 | 1.9142260950770924 | round | PASS | fresh:e3_policies |  |
| 192 | tab-loss-no_singular | 7.58 | 7.58 | 7.5800764027177 | round | PASS | fresh:e3_policies |  |
| 192 | tab-loss-no_singular | 13.14 | 13.14 | 13.135372583414737 | round | PASS | fresh:e3_policies |  |
| 192 | tab-loss-no_singular | 0.043 | 0.043 | 0.04282974541252308 | round | PASS | fresh:e3_policies |  |
| 192 | tab-loss-no_singular | 0.168 | 0.168 | 0.1679272142954109 | round | PASS | fresh:e3_policies |  |
| 192 | tab-loss-no_singular | 0.301 | 0.301 | 0.3005429688236043 | round | PASS | fresh:e3_policies |  |
| 217 | gainform-check | 10^{-14} | 1e-14 | 1.226796442210798e-14 | round | PASS | fresh:e3_policies |  |
| 218 | nosing-diag | 61 | 61 | 60.69651741293532 | round | PASS | fresh:e3_policies |  |
| 218 | nosing-diag | 0.99 | 0.99 | 0.9875 | round | PASS | fresh:e3_policies |  |
| 219 | nosing-diag-contig | (statement) |  |  | conclusion | PASS | fresh:e3_maps | diagonal nodes stopped exactly for x >= 0.9875 |
| 220 | pol-c-concentrated | (statement) |  |  | conclusion | PASS | fresh:e3_maps | no_singular: 43% of the loss in 19% of the window (region: \|x1-x2\|<=0.25) |
| 220 | nosing-loss | 1.9 | 1.9 | 1.9142260950770924 | round | PASS | fresh:e3_policies |  |
| 220 | nosing-loss | 13.1 | 13.1 | 13.135372583414737 | round | PASS | fresh:e3_policies |  |
| 227 | psi-formula | one |  |  | conclusion | PASS | fresh:e3_policies,live:quadrature of psi_eps'' | max \|integral - 1\| = 0.0e+00 over eps in [0.8, 0.4, 0.2, 0.1, 0.05, 0.025]; formula matches the second difference of psi to 2.0e-06 |
| 229 | smooth-bound | (statement) |  |  | conclusion | PASS | fresh:e3_policies,live:fd.Model(N=241).solve() | sup(G_eps-G)/(eps/2) = 1.000000000000014; max abs loss / eps = 0.26 |
| 230 | smooth-negligible | 0.1 | 0.1 | 0.1 | exact | PASS | fresh:e3_policies | largest eps with no diagonal node stopped |
| 230 | smooth-rapid | (statement) |  |  | conclusion | PASS | fresh:e3_policies | mean loss reduced by factors ['3.4', '4.1', '7.9', '18.2', '14.7'] per halving of eps (criterion >= 3); mean loss < 0.01% for eps <= 0.1: True; diagonal stopped iff eps > 0.1: True |
| 238 | tab-smooth-cap | 241 | 241.0 | 241.0 | exact | PASS | fresh:e3_policies,live:fd.Model(N=241).solve() |  |
| 238 | tab-smooth-cap | 0 | 0.0 | 0.0 | exact | PASS | fresh:e3_policies,live:fd.Model(N=241).solve() |  |
| 238 | tab-smooth-cap | 2.5 | 2.5 | 2.5 | exact | PASS | fresh:e3_policies,live:fd.Model(N=241).solve() |  |
| 238 | tab-smooth-cap | 0 | -5.208242914012118e-05 | -5.208242914012118e-05 | le | PASS | fresh:e3_policies,live:fd.Model(N=241).solve() |  |
| 246 | tab-smooth-0.8 | 0.375 | 0.375 | 0.37544743274767234 | round | PASS | fresh:e3_policies |  |
| 246 | tab-smooth-0.8 | 6.32 | 6.32 | 6.320136013013812 | round | PASS | fresh:e3_policies |  |
| 246 | tab-smooth-0.8 | 0.0088 | 0.0088 | 0.008796229814521404 | round | PASS | fresh:e3_policies |  |
| 246 | tab-smooth-0.8 | 0.153 | 0.153 | 0.15348345757209714 | round | PASS | fresh:e3_policies |  |
| 246 | tab-smooth-0.8 | 0.49 | 0.49 | 0.4925373134328358 | round | PASS | fresh:e3_policies |  |
| 247 | tab-smooth-0.4 | 0.109 | 0.109 | 0.1094844068421436 | round | PASS | fresh:e3_policies |  |
| 247 | tab-smooth-0.4 | 3.81 | 3.81 | 3.8066284591646666 | round | PASS | fresh:e3_policies |  |
| 247 | tab-smooth-0.4 | 0.0027 | 0.0027 | 0.002735046380553406 | round | PASS | fresh:e3_policies |  |
| 247 | tab-smooth-0.4 | 0.097 | 0.097 | 0.09695303923300291 | round | PASS | fresh:e3_policies |  |
| 247 | tab-smooth-0.4 | 0.42 | 0.42 | 0.4228855721393035 | round | PASS | fresh:e3_policies |  |
| 248 | tab-smooth-0.2 | 0.027 | 0.027 | 0.026950455939550675 | round | PASS | fresh:e3_policies |  |
| 248 | tab-smooth-0.2 | 1.85 | 1.85 | 1.847767730464022 | round | PASS | fresh:e3_policies |  |
| 248 | tab-smooth-0.2 | 0.0008 | 0.0008 | 0.0007628669655374697 | round | PASS | fresh:e3_policies |  |
| 248 | tab-smooth-0.2 | 0.052 | 0.052 | 0.052005524860499364 | round | PASS | fresh:e3_policies |  |
| 248 | tab-smooth-0.2 | 0.30 | 0.30 | 0.29850746268656714 | round | PASS | fresh:e3_policies |  |
| 249 | tab-smooth-0.1 | 0.003 | 0.003 | 0.0034278477528751003 | round | PASS | fresh:e3_policies |  |
| 249 | tab-smooth-0.1 | 0.31 | 0.31 | 0.3100749626544315 | round | PASS | fresh:e3_policies |  |
| 249 | tab-smooth-0.1 | 0.0001 | 0.0001 | 0.00010563552395118128 | round | PASS | fresh:e3_policies |  |
| 249 | tab-smooth-0.1 | 0.011 | 0.011 | 0.01093737025649233 | round | PASS | fresh:e3_policies |  |
| 249 | tab-smooth-0.1 | 0 | 0 | 0.0 | round | PASS | fresh:e3_policies |  |
| 250 | tab-smooth-0.05 | 2\times10^{-4} | 2e-4 | 0.00018793845105969832 | round | PASS | fresh:e3_policies |  |
| 250 | tab-smooth-0.05 | 0.017 | 0.017 | 0.01669132827543005 | round | PASS | fresh:e3_policies |  |
| 250 | tab-smooth-0.05 | 6\times10^{-6} | 6e-6 | 5.7804876220479e-06 | round | PASS | fresh:e3_policies |  |
| 250 | tab-smooth-0.05 | 6\times10^{-4} | 6e-4 | 0.00057386019435679 | round | PASS | fresh:e3_policies |  |
| 250 | tab-smooth-0.05 | 0 | 0 | 0.0 | round | PASS | fresh:e3_policies |  |
| 251 | tab-smooth-0.025 | 1\times10^{-5} | 1e-5 | 1.2794278655328236e-05 | round | PASS | fresh:e3_policies |  |
| 251 | tab-smooth-0.025 | 0.003 | 0.003 | 0.002799558570003244 | round | PASS | fresh:e3_policies |  |
| 251 | tab-smooth-0.025 | 4\times10^{-7} | 4e-7 | 3.853001344502762e-07 | round | PASS | fresh:e3_policies |  |
| 251 | tab-smooth-0.025 | 9\times10^{-5} | 9e-5 | 9.133815541151336e-05 | round | PASS | fresh:e3_policies |  |
| 251 | tab-smooth-0.025 | 0 | 0 | 0.0 | round | PASS | fresh:e3_policies |  |
| 267 | bias-delta-enlarges | 0 |  |  | conclusion | PASS | live:fd.Model(N=241).solve() | continuation nodes for delta = -0.1, 0, 0.1: [14093, 17586, 21499] |
| 268 | bias-text | -0.046 | -0.046 | -0.045850411575134864 | round | PASS | fresh:e3c_bias |  |
| 268 | bias-text | -0.022 | -0.022 | -0.022394331286060998 | round | PASS | fresh:e3c_bias |  |
| 268 | bias-text | -0.012 | -0.012 | -0.011572510228801958 | round | PASS | fresh:e3c_bias |  |
| 268 | bias-text | 121 | 121.0 | 121.0 | exact | PASS | fresh:e3c_bias |  |
| 268 | bias-text | 241 | 241.0 | 241.0 | exact | PASS | fresh:e3c_bias |  |
| 268 | bias-text | 481 | 481.0 | 481.0 | exact | PASS | fresh:e3c_bias |  |
| 269 | bias-halves | halves |  |  | conclusion | PASS | fresh:e3c_bias | successive ratios ['2.047', '1.935'], observed orders ['1.034', '0.952'] (criterion: \|order - 1\| <= 0.25) |
| 270 | bias-zero-limit | (statement) |  |  | conclusion | PASS | fresh:e3c_bias | Richardson extrapolation 2B(h/2)-B(h) = 1.06e-03, -7.51e-04 |
| 270 | bias-order-one | one |  |  | conclusion | PASS | fresh:e3c_bias | \|B\| for shifted boundaries in [0.210, 1.042] (criterion: within [0.1, 10] and >= 5 \|B(0)\| = 0.112); sign = sign(delta): True |
| 283 | tab-bias-241--0.20 | -0.2266 | -0.2266 | -0.22656674003357402 | round | PASS | fresh:e3c_bias |  |
| 283 | tab-bias-241--0.20 | -1.2683 | -1.2683 | -1.2682780603008574 | round | PASS | fresh:e3c_bias |  |
| 283 | tab-bias-241--0.20 | -1.0417 | -1.0417 | -1.0417113202672834 | round | PASS | fresh:e3c_bias |  |
| 284 | tab-bias-241--0.10 | -0.2626 | -0.2626 | -0.26264336916777586 | round | PASS | fresh:e3c_bias |  |
| 284 | tab-bias-241--0.10 | -0.7527 | -0.7527 | -0.7526943855024694 | round | PASS | fresh:e3c_bias |  |
| 284 | tab-bias-241--0.10 | -0.4901 | -0.4901 | -0.4900510163346935 | round | PASS | fresh:e3c_bias |  |
| 285 | tab-bias-241--0.05 | -0.2723 | -0.2723 | -0.2722732488088553 | round | PASS | fresh:e3c_bias |  |
| 285 | tab-bias-241--0.05 | -0.5064 | -0.5064 | -0.5064228386112836 | round | PASS | fresh:e3c_bias |  |
| 285 | tab-bias-241--0.05 | -0.2341 | -0.2341 | -0.23414958980242828 | round | PASS | fresh:e3c_bias |  |
| 286 | tab-bias-241-0.05 | -0.2703 | -0.2703 | -0.2702723917959906 | round | PASS | fresh:e3c_bias |  |
| 286 | tab-bias-241-0.05 | -0.0598 | -0.0598 | -0.059847925962173844 | round | PASS | fresh:e3c_bias |  |
| 286 | tab-bias-241-0.05 | 0.2104 | 0.2104 | 0.21042446583381677 | round | PASS | fresh:e3c_bias |  |
| 287 | tab-bias-241-0.10 | -0.2566 | -0.2566 | -0.2566210069835202 | round | PASS | fresh:e3c_bias |  |
| 287 | tab-bias-241-0.10 | 0.1358 | 0.1358 | 0.13578648091029744 | round | PASS | fresh:e3c_bias |  |
| 287 | tab-bias-241-0.10 | 0.3924 | 0.3924 | 0.39240748789381763 | round | PASS | fresh:e3c_bias |  |
| 288 | tab-bias-241-0.20 | -0.1987 | -0.1987 | -0.19874528458576668 | round | PASS | fresh:e3c_bias |  |
| 288 | tab-bias-241-0.20 | 0.4664 | 0.4664 | 0.4663509706359261 | round | PASS | fresh:e3c_bias |  |
| 288 | tab-bias-241-0.20 | 0.6651 | 0.6651 | 0.6650962552216928 | round | PASS | fresh:e3c_bias |  |
| 290 | tab-bias-121-0 | -0.2752 | -0.2752 | -0.27521131228517404 | round | PASS | fresh:e3c_bias |  |
| 290 | tab-bias-121-0 | -0.3211 | -0.3211 | -0.3210617238603089 | round | PASS | fresh:e3c_bias |  |
| 290 | tab-bias-121-0 | -0.0459 | -0.0459 | -0.045850411575134864 | round | PASS | fresh:e3c_bias |  |
| 291 | tab-bias-241-0 | -0.2752 | -0.2752 | -0.2751869254730297 | round | PASS | fresh:e3c_bias |  |
| 291 | tab-bias-241-0 | -0.2976 | -0.2976 | -0.2975812567590907 | round | PASS | fresh:e3c_bias |  |
| 291 | tab-bias-241-0 | -0.0224 | -0.0224 | -0.022394331286060998 | round | PASS | fresh:e3c_bias |  |
| 292 | tab-bias-481-0 | -0.2752 | -0.2752 | -0.27518152758742787 | round | PASS | fresh:e3c_bias |  |
| 292 | tab-bias-481-0 | -0.2868 | -0.2868 | -0.2867540378162298 | round | PASS | fresh:e3c_bias |  |
| 292 | tab-bias-481-0 | -0.0116 | -0.0116 | -0.011572510228801958 | round | PASS | fresh:e3c_bias |  |
| 298 | post-setup | 481 | 481.0 | 481.0 | exact | PASS | fresh:baseline481 |  |
| 300 | post-setup2 | 120 | 120.0 | 120.0 | exact | PASS | fresh:e5_post |  |
| 300 | post-setup2 | 2\times10^4 | 20000.0 | 20000.0 | exact | PASS | fresh:e5_post |  |
| 300 | post-setup2 | 0.005 | 0.005 | 0.005 | exact | PASS | fresh:e5_post |  |
| 303 | post-fine | 0.0006 | 0.0006 | 0.0006140407668527951 | round | PASS | fresh:e5_post |  |
| 303 | post-fine | 0.0081 | 0.0081 | 0.008090453210173076 | round | PASS | fresh:e5_post |  |
| 303 | post-fine | 0.455 | 0.455 | 0.45517677901841364 | round | PASS | fresh:e5_post |  |
| 303 | post-fine | 0.005 | 0.005 | 0.005065298407545278 | round | PASS | fresh:e5_post |  |
| 305 | post-ci95 | 95 | 95 | 95.0004209703559 | round | PASS |  | coverage of the 1.96 sd interval used in mc.ci |
| 305 | post-coarse | 0.01 | 0.01 | 0.01 | exact | PASS | fresh:e5_post |  |
| 305 | post-coarse | 0.0094 | 0.0094 | 0.009442563052382663 | round | PASS | fresh:e5_post |  |
| 305 | post-coarse | 0.0079 | 0.0079 | 0.007880424373748656 | round | PASS | fresh:e5_post |  |
| 305 | post-coarse | 0.445 | 0.445 | 0.44541707653568363 | round | PASS | fresh:e5_post |  |
| 305 | post-coarse | 0.005 | 0.005 | 0.0048998300748036225 | round | PASS | fresh:e5_post |  |
| 306 | post-bias-visible | (statement) |  |  | conclusion | PASS | fresh:e5_post | E[Z] - halfwidth = 0.0016 > 0 at dt = 0.01 |
| 307 | post-horizon | 200 | 200.0 | 200.0 | exact | PASS | fresh:e5_post |  |
| 307 | post-horizon | 0.01 | 0.01 | 0.01 | exact | PASS | fresh:e5_post |  |
| 307 | post-horizon | 4\times10^{-4} | 0.00035205716200040205 | 0.00035205716200040205 | lt | PASS | fresh:e5_post |  |
| 308 | post-discount | 2.5\times10^{-3} | 2.5e-3 | 0.0024787521766663585 | round | PASS |  |  |
| 308 | post-discount | 120 | 120.0 | 120.0 | exact | PASS |  |  |
| 309 | post-order-one | one |  |  | conclusion | PASS | fresh:e5_post | E\|Z\| = 0.455 |
| 310 | post-zero | (statement) |  |  | conclusion | PASS | fresh:e5_post | \|E[Z]\| = 0.0006 <= half-width 0.0081 at dt = 0.005 |
| 317 | statics-grid | 4 | 4.0 | 4.0 | exact | PASS |  |  |
| 317 | statics-grid | 321 | 321.0 | 321.0 | exact | PASS |  |  |
| 317 | statics-grid | 0.0125 | 0.0125 | 0.0125 | exact | PASS |  |  |
| 317 | statics-grid | 241 | 241.0 | 241.0 | exact | PASS |  |  |
| 318 | statics-same-h | (statement) |  |  | conclusion | PASS |  | h = 4/320 = 0.012500000000000001, 3/240 = 0.012500000000000001 |
| 319 | statics-mono | (statement) |  |  | conclusion | PASS | fresh:e4_statics | areas and widths decrease, Gamma_ac increases: [True, True, np.True_] |
| 320 | statics-alpha-arms | (statement) |  |  | conclusion | PASS | fresh:e4_statics | area(D1) - area(D2): [1.576, 0.0, -1.502] |
| 321 | statics-q-linear | 0.576 | 0.576 | 0.5760000000000001 | round | PASS | fresh:e4_statics |  |
| 321 | statics-q-linear | -0.8 | -0.8 | -0.8 | exact | PASS | fresh:e4_statics |  |
| 321 | statics-q-linear | 0.064 | 0.064 | 0.064 | round | PASS | fresh:e4_statics |  |
| 321 | statics-q-linear | 0.8 | 0.8 | 0.8 | exact | PASS | fresh:e4_statics |  |
| 321 | statics-q-linear-chk | (statement) |  |  | conclusion | PASS | fresh:e4_statics | slopes [-0.32] (spread 3.9e-16) |
| 322 | statics-decrease-q | (statement) |  |  | conclusion | PASS | fresh:e4_statics | both increasing in q over the rho sweep |
| 323 | statics-premium-pct | 2 | 2.0 | 2.0 | exact | PASS | fresh:e4_statics |  |
| 323 | statics-premium-pct | 2 | 2.0 | 2.0 | exact | PASS | fresh:e4_statics |  |
| 323 | statics-premium-pct | 3 | 2.5622901588636338 | 2.5622901588636338 | le | PASS | fresh:e4_statics |  |
| 324 | statics-hw-sym | 3 | 3 | 2.797740633408785 | round | PASS | fresh:e4_statics |  |
| 324 | statics-hw-sym | 16 | 16 | 16.017551176980447 | round | PASS | fresh:e4_statics |  |
| 325 | statics-two-cells | 0.8 | 0.8 | 0.8 | exact | PASS |  |  |
| 325 | statics-two-cells-chk | two |  |  | conclusion | PASS | fresh:e4_statics | half-width / h = 2.108 |
| 326 | statics-asym | 5 | 5 | 5.425641317472374 | round | PASS | fresh:e4_statics |  |
| 326 | statics-asym | 12 | 12 | 11.690251629331206 | round | PASS | fresh:e4_statics |  |
| 333 | statics-cap | 4 | 4.0 | 4.0 | exact | PASS |  |  |
| 333 | statics-cap | 321 | 321.0 | 321.0 | exact | PASS |  |  |
| 333 | statics-cap | 0.0125 | 0.0125 | 0.0125 | exact | PASS |  |  |
| 333 | statics-cap | 0 | 0.0 | 0.0 | exact | PASS |  |  |
| 333 | statics-cap | 2.5 | 2.5 | 2.5 | exact | PASS |  |  |
| 335 | statics-cap-G | 2 | 2.0 | 2.0 | exact | PASS |  |  |
| 343 | tab-statics-alpha-0.7 | 0.238 | 0.238 | 0.23840000000000003 | round | PASS | fresh:e4_statics |  |
| 343 | tab-statics-alpha-0.7 | 2.74 | 2.74 | 2.7434375000000006 | round | PASS | fresh:e4_statics |  |
| 343 | tab-statics-alpha-0.7 | 2.57 | 2.57 | 2.5726562500000005 | round | PASS | fresh:e4_statics |  |
| 343 | tab-statics-alpha-0.7 | 1.00 | 1.00 | 0.9965625000000002 | round | PASS | fresh:e4_statics |  |
| 343 | tab-statics-alpha-0.7 | 0.104 | 0.104 | 0.10408249966900396 | round | PASS | fresh:e4_statics |  |
| 343 | tab-statics-alpha-0.7 | 0.094 | 0.094 | 0.09419242821387863 | round | PASS | fresh:e4_statics |  |
| 343 | tab-statics-alpha-0.7 | 0.111 | 0.111 | 0.11069494131077452 | round | PASS | fresh:e4_statics |  |
| 343 | tab-statics-alpha-0.7 | 0.100 | 0.100 | 0.09959615854236868 | round | PASS | fresh:e4_statics |  |
| 343 | tab-statics-alpha-0.7 | 0.0243 | 0.0243 | 0.024264742057390834 | round | PASS | fresh:e4_statics |  |
| 344 | tab-statics-alpha-1 | 0.320 | 0.320 | 0.32000000000000006 | round | PASS | fresh:e4_statics |  |
| 344 | tab-statics-alpha-1 | 2.66 | 2.66 | 2.6592187500000004 | round | PASS | fresh:e4_statics |  |
| 344 | tab-statics-alpha-1 | 1.83 | 1.83 | 1.8267187500000004 | round | PASS | fresh:e4_statics |  |
| 344 | tab-statics-alpha-1 | 1.83 | 1.83 | 1.8267187500000004 | round | PASS | fresh:e4_statics |  |
| 344 | tab-statics-alpha-1 | 0.147 | 0.147 | 0.1466770484663087 | round | PASS | fresh:e4_statics |  |
| 344 | tab-statics-alpha-1 | 0.147 | 0.147 | 0.1466770484663087 | round | PASS | fresh:e4_statics |  |
| 344 | tab-statics-alpha-1 | 0.157 | 0.157 | 0.156862744994233 | round | PASS | fresh:e4_statics |  |
| 344 | tab-statics-alpha-1 | 0.157 | 0.157 | 0.15686274506343717 | round | PASS | fresh:e4_statics |  |
| 344 | tab-statics-alpha-1 | 0.0398 | 0.0398 | 0.03981089468117238 | round | PASS | fresh:e4_statics |  |
| 345 | tab-statics-alpha-1.4 | 0.474 | 0.474 | 0.4736 | round | PASS | fresh:e4_statics |  |
| 345 | tab-statics-alpha-1.4 | 2.77 | 2.77 | 2.7668750000000006 | round | PASS | fresh:e4_statics |  |
| 345 | tab-statics-alpha-1.4 | 1.02 | 1.02 | 1.021875 | round | PASS | fresh:e4_statics |  |
| 345 | tab-statics-alpha-1.4 | 2.52 | 2.52 | 2.5239062500000005 | round | PASS | fresh:e4_statics |  |
| 345 | tab-statics-alpha-1.4 | 0.233 | 0.233 | 0.23302801289958408 | round | PASS | fresh:e4_statics |  |
| 345 | tab-statics-alpha-1.4 | 0.271 | 0.271 | 0.2707048367165332 | round | PASS | fresh:e4_statics |  |
| 345 | tab-statics-alpha-1.4 | 0.254 | 0.254 | 0.2539430328490119 | round | PASS | fresh:e4_statics |  |
| 345 | tab-statics-alpha-1.4 | 0.307 | 0.307 | 0.30654015180779876 | round | PASS | fresh:e4_statics |  |
| 345 | tab-statics-alpha-1.4 | 0.0735 | 0.0735 | 0.07352749708999116 | round | PASS | fresh:e4_statics |  |
| 346 | tab-statics-r-0.03 | 0.320 | 0.320 | 0.32000000000000006 | round | PASS | fresh:e4_statics |  |
| 346 | tab-statics-r-0.03 | 3.00 | 3.00 | 3.0032812500000006 | round | PASS | fresh:e4_statics |  |
| 346 | tab-statics-r-0.03 | 1.65 | 1.65 | 1.6546875000000003 | round | PASS | fresh:e4_statics |  |
| 346 | tab-statics-r-0.03 | 1.65 | 1.65 | 1.6546875000000003 | round | PASS | fresh:e4_statics |  |
| 346 | tab-statics-r-0.03 | 0.159 | 0.159 | 0.1586457907925971 | round | PASS | fresh:e4_statics |  |
| 346 | tab-statics-r-0.03 | 0.159 | 0.159 | 0.1586457907926011 | round | PASS | fresh:e4_statics |  |
| 346 | tab-statics-r-0.03 | 0.170 | 0.170 | 0.17021276584065193 | round | PASS | fresh:e4_statics |  |
| 346 | tab-statics-r-0.03 | 0.170 | 0.170 | 0.1702127659185152 | round | PASS | fresh:e4_statics |  |
| 346 | tab-statics-r-0.03 | 0.0437 | 0.0437 | 0.04372490436109455 | round | PASS | fresh:e4_statics |  |
| 347 | tab-statics-r-0.08 | 0.320 | 0.320 | 0.32000000000000006 | round | PASS | fresh:e4_statics |  |
| 347 | tab-statics-r-0.08 | 2.31 | 2.31 | 2.3110937500000004 | round | PASS | fresh:e4_statics |  |
| 347 | tab-statics-r-0.08 | 2.00 | 2.00 | 2.00078125 | round | PASS | fresh:e4_statics |  |
| 347 | tab-statics-r-0.08 | 2.00 | 2.00 | 2.00078125 | round | PASS | fresh:e4_statics |  |
| 347 | tab-statics-r-0.08 | 0.130 | 0.130 | 0.13045298712907272 | round | PASS | fresh:e4_statics |  |
| 347 | tab-statics-r-0.08 | 0.130 | 0.130 | 0.13045298712905185 | round | PASS | fresh:e4_statics |  |
| 347 | tab-statics-r-0.08 | 0.140 | 0.140 | 0.1403508771043398 | round | PASS | fresh:e4_statics |  |
| 347 | tab-statics-r-0.08 | 0.140 | 0.140 | 0.14035087716343492 | round | PASS | fresh:e4_statics |  |
| 347 | tab-statics-r-0.08 | 0.0353 | 0.0353 | 0.03533382071486546 | round | PASS | fresh:e4_statics |  |
| 348 | tab-statics-c0-0.005 | 0.320 | 0.320 | 0.32000000000000006 | round | PASS | fresh:e4_statics |  |
| 348 | tab-statics-c0-0.005 | 2.71 | 2.71 | 2.7139062500000004 | round | PASS | fresh:e4_statics |  |
| 348 | tab-statics-c0-0.005 | 1.80 | 1.80 | 1.7993750000000004 | round | PASS | fresh:e4_statics |  |
| 348 | tab-statics-c0-0.005 | 1.80 | 1.80 | 1.7993750000000004 | round | PASS | fresh:e4_statics |  |
| 348 | tab-statics-c0-0.005 | 0.148 | 0.148 | 0.14833068104157388 | round | PASS | fresh:e4_statics |  |
| 348 | tab-statics-c0-0.005 | 0.148 | 0.148 | 0.14833068104158942 | round | PASS | fresh:e4_statics |  |
| 348 | tab-statics-c0-0.005 | 0.158 | 0.158 | 0.15841584147828647 | round | PASS | fresh:e4_statics |  |
| 348 | tab-statics-c0-0.005 | 0.158 | 0.158 | 0.1584158415488678 | round | PASS | fresh:e4_statics |  |
| 348 | tab-statics-c0-0.005 | 0.0402 | 0.0402 | 0.040248694195537116 | round | PASS | fresh:e4_statics |  |
| 349 | tab-statics-c0-0.03 | 0.320 | 0.320 | 0.32000000000000006 | round | PASS | fresh:e4_statics |  |
| 349 | tab-statics-c0-0.03 | 2.46 | 2.46 | 2.4642187500000006 | round | PASS | fresh:e4_statics |  |
| 349 | tab-statics-c0-0.03 | 1.92 | 1.92 | 1.9242187500000003 | round | PASS | fresh:e4_statics |  |
| 349 | tab-statics-c0-0.03 | 1.92 | 1.92 | 1.9242187500000003 | round | PASS | fresh:e4_statics |  |
| 349 | tab-statics-c0-0.03 | 0.141 | 0.141 | 0.14116403883872009 | round | PASS | fresh:e4_statics |  |
| 349 | tab-statics-c0-0.03 | 0.141 | 0.141 | 0.14116403883876583 | round | PASS | fresh:e4_statics |  |
| 349 | tab-statics-c0-0.03 | 0.151 | 0.151 | 0.1509433961302955 | round | PASS | fresh:e4_statics |  |
| 349 | tab-statics-c0-0.03 | 0.151 | 0.151 | 0.15094339619437527 | round | PASS | fresh:e4_statics |  |
| 349 | tab-statics-c0-0.03 | 0.0382 | 0.0382 | 0.03818080674002067 | round | PASS | fresh:e4_statics |  |
| 350 | tab-statics-rho--0.8 | 0.576 | 0.576 | 0.5760000000000001 | round | PASS | fresh:e4_statics |  |
| 350 | tab-statics-rho--0.8 | 3.12 | 3.12 | 3.1164062500000007 | round | PASS | fresh:e4_statics |  |
| 350 | tab-statics-rho--0.8 | 1.60 | 1.60 | 1.5981250000000002 | round | PASS | fresh:e4_statics |  |
| 350 | tab-statics-rho--0.8 | 1.60 | 1.60 | 1.5981250000000002 | round | PASS | fresh:e4_statics |  |
| 350 | tab-statics-rho--0.8 | 0.250 | 0.250 | 0.25005814488416966 | round | PASS | fresh:e4_statics |  |
| 350 | tab-statics-rho--0.8 | 0.250 | 0.250 | 0.25005814488417544 | round | PASS | fresh:e4_statics |  |
| 350 | tab-statics-rho--0.8 | 0.282 | 0.282 | 0.2823529409896194 | round | PASS | fresh:e4_statics |  |
| 350 | tab-statics-rho--0.8 | 0.282 | 0.282 | 0.28235294111418685 | round | PASS | fresh:e4_statics |  |
| 350 | tab-statics-rho--0.8 | 0.0719 | 0.0719 | 0.07191181093301058 | round | PASS | fresh:e4_statics |  |
| 351 | tab-statics-rho--0.4 | 0.448 | 0.448 | 0.44800000000000006 | round | PASS | fresh:e4_statics |  |
| 351 | tab-statics-rho--0.4 | 2.90 | 2.90 | 2.8970312500000004 | round | PASS | fresh:e4_statics |  |
| 351 | tab-statics-rho--0.4 | 1.71 | 1.71 | 1.7078125000000004 | round | PASS | fresh:e4_statics |  |
| 351 | tab-statics-rho--0.4 | 1.71 | 1.71 | 1.7078125000000004 | round | PASS | fresh:e4_statics |  |
| 351 | tab-statics-rho--0.4 | 0.200 | 0.200 | 0.19958527754609978 | round | PASS | fresh:e4_statics |  |
| 351 | tab-statics-rho--0.4 | 0.200 | 0.200 | 0.19958527754609978 | round | PASS | fresh:e4_statics |  |
| 351 | tab-statics-rho--0.4 | 0.220 | 0.220 | 0.2196078429919262 | round | PASS | fresh:e4_statics |  |
| 351 | tab-statics-rho--0.4 | 0.220 | 0.220 | 0.219607843088812 | round | PASS | fresh:e4_statics |  |
| 351 | tab-statics-rho--0.4 | 0.0559 | 0.0559 | 0.0558933733402287 | round | PASS | fresh:e4_statics |  |
| 352 | tab-statics-rho-0.4 | 0.192 | 0.192 | 0.19200000000000003 | round | PASS | fresh:e4_statics |  |
| 352 | tab-statics-rho-0.4 | 2.39 | 2.39 | 2.3923437500000007 | round | PASS | fresh:e4_statics |  |
| 352 | tab-statics-rho-0.4 | 1.96 | 1.96 | 1.9601562500000005 | round | PASS | fresh:e4_statics |  |
| 352 | tab-statics-rho-0.4 | 1.96 | 1.96 | 1.9601562500000005 | round | PASS | fresh:e4_statics |  |
| 352 | tab-statics-rho-0.4 | 0.090 | 0.090 | 0.09004787345100196 | round | PASS | fresh:e4_statics |  |
| 352 | tab-statics-rho-0.4 | 0.090 | 0.090 | 0.09004787345100951 | round | PASS | fresh:e4_statics |  |
| 352 | tab-statics-rho-0.4 | 0.094 | 0.094 | 0.0941176469965398 | round | PASS | fresh:e4_statics |  |
| 352 | tab-statics-rho-0.4 | 0.094 | 0.094 | 0.0941176470380623 | round | PASS | fresh:e4_statics |  |
| 352 | tab-statics-rho-0.4 | 0.0237 | 0.0237 | 0.023728307730755294 | round | PASS | fresh:e4_statics |  |
| 353 | tab-statics-rho-0.8 | 0.064 | 0.064 | 0.064 | round | PASS | fresh:e4_statics |  |
| 353 | tab-statics-rho-0.8 | 2.08 | 2.08 | 2.07546875 | round | PASS | fresh:e4_statics |  |
| 353 | tab-statics-rho-0.8 | 2.12 | 2.12 | 2.1185937500000005 | round | PASS | fresh:e4_statics |  |
| 353 | tab-statics-rho-0.8 | 2.12 | 2.12 | 2.1185937500000005 | round | PASS | fresh:e4_statics |  |
| 353 | tab-statics-rho-0.8 | 0.026 | 0.026 | 0.026347434907433076 | round | PASS | fresh:e4_statics |  |
| 353 | tab-statics-rho-0.8 | 0.026 | 0.026 | 0.026347434907433076 | round | PASS | fresh:e4_statics |  |
| 353 | tab-statics-rho-0.8 | 0.031 | 0.031 | 0.031372548998846596 | round | PASS | fresh:e4_statics |  |
| 353 | tab-statics-rho-0.8 | 0.031 | 0.031 | 0.03137254901268743 | round | PASS | fresh:e4_statics |  |
| 353 | tab-statics-rho-0.8 | 0.0076 | 0.0076 | 0.007642173320866696 | round | PASS | fresh:e4_statics |  |
| 363 | fig-rho-cap | -0.8 | -0.8 | -0.8 | exact | PASS | fresh:e4_statics |  |
| 363 | fig-rho-cap | -0.6 | -0.6 | -0.6 | exact | PASS | fresh:e4_statics |  |
| 363 | fig-rho-cap | 0.8 | 0.8 | 0.8 | exact | PASS | fresh:e4_statics |  |
| 363 | fig-rho-cap | 0.0125 | 0.0125 | 0.0125 | exact | PASS | fresh:e4_statics |  |
| 363 | fig-rho-cap-step | (statement) |  |  | conclusion | PASS | fresh:e4_statics | rho values [-0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8] |
| 363 | fig-rho-pts | 2 | 2.0 | 2.0 | exact | PASS |  |  |
| 363 | fig-rho-pts | 2 | 2.0 | 2.0 | exact | PASS |  |  |
| 363 | fig-rho-pts | 2 | 2.0 | 2.0 | exact | PASS |  |  |
| 363 | fig-rho-pts | 2 | 2.0 | 2.0 | exact | PASS |  |  |
| 373 | mc-xref | 0.9 | 0.9 | 0.9 | exact | PASS | fresh:baseline481 |  |
| 373 | mc-xref | 1.0 | 1.0 | 1.0 | exact | PASS | fresh:baseline481 |  |
| 373 | mc-xref | 481 | 481.0 | 481.0 | exact | PASS | fresh:baseline481 |  |
| 375 | mc-P | -0.2752 | -0.2752 | -0.27518152758742787 | round | PASS | fresh:e1_refinement |  |
| 375 | mc-Y0 | 0.1 | 0.1 | 0.09999999999999998 | round | PASS |  |  |
| 376 | mc-M | 2\times10^5 | 200000.0 | 200000.0 | exact | PASS | fresh:e5_mc |  |
| 376 | mc-M | 40 | 40.0 | 40.0 | exact | PASS | fresh:e5_mc |  |
| 377 | mc-tau | 3.6 | 3.6 | 3.6031829374999997 | round | PASS | fresh:e5_mc |  |
| 377 | mc-tau | 3.9 | 3.9 | 3.9146278000000003 | round | PASS | fresh:e5_mc |  |
| 377 | mc-alive | 5\times10^{-5} | 4e-05 | 4e-05 | lt | PASS | fresh:e5_mc |  |
| 379 | mc-disc | 0.135 | 0.135 | 0.1353352832366127 | round | PASS | fresh:e5_mc |  |
| 384 | mc-cap | 95 | 95 | 95.0004209703559 | round | PASS | fresh:e1_refinement,fresh:e5_mc |  |
| 384 | mc-cap | 2\times10^5 | 200000.0 | 200000.0 | exact | PASS | fresh:e1_refinement,fresh:e5_mc |  |
| 384 | mc-cap | -0.2752 | -0.2752 | -0.27518152758742787 | round | PASS | fresh:e1_refinement,fresh:e5_mc |  |
| 392 | mc-header | 2 0.4 |  |  | conclusion | PASS | fresh:e5_mc | bandwidths in the output equal (1/2, 1, 2) sqrt(dt) and dt^0.4 bitwise |
| 394 | tab-mc-0.02 | -0.2735 | -0.2735 | -0.27352892802086326 | round | PASS | fresh:e5_mc |  |
| 394 | tab-mc-0.02 | 0.0011 | 0.0011 | 0.0010703937626285103 | round | PASS | fresh:e5_mc |  |
| 394 | tab-mc-0.02 | -0.2687 | -0.2687 | -0.2687093072470345 | round | PASS | fresh:e5_mc |  |
| 394 | tab-mc-0.02 | -0.2711 | -0.2711 | -0.2711435468061159 | round | PASS | fresh:e5_mc |  |
| 394 | tab-mc-0.02 | -0.2307 | -0.2307 | -0.23065472992803313 | round | PASS | fresh:e5_mc |  |
| 394 | tab-mc-0.02 | -0.2531 | -0.2531 | -0.2530802061130818 | round | PASS | fresh:e5_mc |  |
| 394 | tab-mc-0.02 | 0.0024 | 0.0024 | 0.0023853812147473005 | round | PASS | fresh:e5_mc |  |
| 394 | tab-mc-0.02 | 0.0028 | 0.0028 | 0.002782036754082672 | round | PASS | fresh:e5_mc |  |
| 395 | tab-mc-0.01 | -0.2742 | -0.2742 | -0.2741719692614353 | round | PASS | fresh:e5_mc |  |
| 395 | tab-mc-0.01 | 0.0010 | 0.0010 | 0.001043266696776748 | round | PASS | fresh:e5_mc |  |
| 395 | tab-mc-0.01 | -0.2723 | -0.2723 | -0.2723485751201037 | round | PASS | fresh:e5_mc |  |
| 395 | tab-mc-0.01 | -0.2770 | -0.2770 | -0.27697629385672495 | round | PASS | fresh:e5_mc |  |
| 395 | tab-mc-0.01 | -0.2549 | -0.2549 | -0.25490518781801796 | round | PASS | fresh:e5_mc |  |
| 395 | tab-mc-0.01 | -0.2652 | -0.2652 | -0.26516730575415126 | round | PASS | fresh:e5_mc |  |
| 395 | tab-mc-0.01 | -0.0028 | -0.0028 | -0.002804324595289626 | round | PASS | fresh:e5_mc |  |
| 395 | tab-mc-0.01 | 0.0028 | 0.0028 | 0.0028017064528478605 | round | PASS | fresh:e5_mc |  |
| 396 | tab-mc-0.005 | -0.2754 | -0.2754 | -0.27543123131802977 | round | PASS | fresh:e5_mc |  |
| 396 | tab-mc-0.005 | 0.0010 | 0.0010 | 0.0010194823057648793 | round | PASS | fresh:e5_mc |  |
| 396 | tab-mc-0.005 | -0.2732 | -0.2732 | -0.2731658797762854 | round | PASS | fresh:e5_mc |  |
| 396 | tab-mc-0.005 | -0.2722 | -0.2722 | -0.27220661260822265 | round | PASS | fresh:e5_mc |  |
| 396 | tab-mc-0.005 | -0.2678 | -0.2678 | -0.2677908028147045 | round | PASS | fresh:e5_mc |  |
| 396 | tab-mc-0.005 | -0.2715 | -0.2715 | -0.2714862965453616 | round | PASS | fresh:e5_mc |  |
| 396 | tab-mc-0.005 | 0.0032 | 0.0032 | 0.003224618709807176 | round | PASS | fresh:e5_mc |  |
| 396 | tab-mc-0.005 | 0.0028 | 0.0028 | 0.002801265387612318 | round | PASS | fresh:e5_mc |  |
| 397 | tab-mc-0.0025 | -0.2754 | -0.2754 | -0.2754405645966985 | round | PASS | fresh:e5_mc |  |
| 397 | tab-mc-0.0025 | 0.0010 | 0.0010 | 0.0010041479252919446 | round | PASS | fresh:e5_mc |  |
| 397 | tab-mc-0.0025 | -0.2744 | -0.2744 | -0.27441609531101113 | round | PASS | fresh:e5_mc |  |
| 397 | tab-mc-0.0025 | -0.2740 | -0.2740 | -0.27398835888206746 | round | PASS | fresh:e5_mc |  |
| 397 | tab-mc-0.0025 | -0.2742 | -0.2742 | -0.2741658435276139 | round | PASS | fresh:e5_mc |  |
| 397 | tab-mc-0.0025 | -0.2727 | -0.2727 | -0.272735212381873 | round | PASS | fresh:e5_mc |  |
| 397 | tab-mc-0.0025 | 0.0015 | 0.0015 | 0.0014522057146310692 | round | PASS | fresh:e5_mc |  |
| 397 | tab-mc-0.0025 | 0.0028 | 0.0028 | 0.0028034297657146615 | round | PASS | fresh:e5_mc |  |
| 402 | tab-mc-hw | 0.0017 | 0.0017 | 0.0017199121443821019 | round | PASS | fresh:e5_mc |  |
| 402 | tab-mc-hw | 0.0021 | 0.0021 | 0.0020627479208662806 | round | PASS | fresh:e5_mc |  |
| 410 | fig-mc-cap | 2\times10^5 | 200000.0 | 200000.0 | exact | PASS | fresh:e5_mc |  |
| 410 | fig-mc-cap-four | four |  |  | conclusion | PASS | fresh:e5_mc | 4 time steps |
| 412 | fig-mc-cap2 | 0.005 | 0.005 | 0.005 | exact | PASS |  |  |
| 412 | fig-mc-cap2 | 95 | 95 | 95.0004209703559 | round | PASS |  |  |
| 417 | mc-three | Three |  |  | conclusion | PASS |  | structure of the text (First/Second/Third follow) |
| 417 | mc-direct | -0.2754 | -0.2754 | -0.27543123131802977 | round | PASS | fresh:e5_mc |  |
| 417 | mc-direct | 0.0010 | 0.0010 | 0.0010194823057648793 | round | PASS | fresh:e5_mc |  |
| 417 | mc-direct | 0.005 | 0.005 | 0.005 | exact | PASS | fresh:e5_mc |  |
| 418 | mc-direct-both | (statement) |  |  | conclusion | PASS | fresh:e5_mc | dt=0.005: -0.27543+-0.00102, dt=0.0025: -0.27544+-0.00100 |
| 418 | mc-direct-bias | 0.002 | 0.002 | 0.0016525995665646054 | round | PASS | fresh:e1_refinement,fresh:e5_mc |  |
| 418 | mc-direct-bias | 0.02 | 0.02 | 0.02 | exact | PASS | fresh:e1_refinement,fresh:e5_mc |  |
| 419 | mc-paired | 0.1 | 0.1 | 0.09999999999999998 | round | PASS | fresh:e5_mc |  |
| 419 | mc-paired | 0.005 | 0.004819620773828756 | 0.004819620773828756 | le | PASS | fresh:e5_mc |  |
| 420 | mc-paired-words | one two |  |  | conclusion | PASS | fresh:e5_mc | largest \|paired difference\| / its half-width = 1.68; all ratios ['1.68', '0.64', '0.80', '1.15', '0.36', '0.52', '0.98'] |
| 421 | mc-spread | 0.01 | 0.01 | 0.01 | exact | PASS | fresh:e5_mc |  |
| 421 | mc-spread | 0.05 | 0.05 | 0.05 | exact | PASS | fresh:e5_mc |  |
| 421 | mc-spread | 0.1 | 0.1 | 0.1 | exact | PASS | fresh:e5_mc |  |
| 421 | mc-spread | 0.2 | 0.2 | 0.2 | exact | PASS | fresh:e5_mc |  |
| 421 | mc-spread | -0.2723 | -0.2723 | -0.2723485751201037 | round | PASS | fresh:e5_mc |  |
| 421 | mc-spread | -0.2770 | -0.2770 | -0.27697629385672495 | round | PASS | fresh:e5_mc |  |
| 421 | mc-spread | -0.2549 | -0.2549 | -0.25490518781801796 | round | PASS | fresh:e5_mc |  |
| 421 | mc-spread | 0.022 | 0.022 | 0.02207110603870699 | round | PASS | fresh:e5_mc |  |
| 422 | mc-spread-ten | ten |  |  | conclusion | PASS | fresh:e5_mc | spread / largest half-width = 10.7 |
| 425 | mc-eps-itself | (statement) |  |  | conclusion | PASS | fresh:e5_mc | eps=0.2 at ratios 2 and 4: -0.2549 vs -0.2552; ratio 2 at eps=0.283 and 0.1: -0.2307 vs -0.2742 |
| 426 | mc-third | 0.4 | 0.4 | 0.4000000000000001 | round | PASS | fresh:e5_mc |  |
| 427 | mc-third-conv | (statement) |  |  | conclusion | PASS | fresh:e1_refinement,fresh:e5_mc | errors with eps=dt^0.4: ['0.0221', '0.0100', '0.0037', '0.0024']; with eps=sqrt(dt): ['0.0040', '0.0018', '0.0030', '0.0012'] |
| 432 | mc-scaling | (statement) |  |  | conclusion | PASS | fresh:e5_mc_M | fitted exponent -0.4961 (criterion \|exponent + 1/2\| <= 0.05) |
| 439 | alg-nodes | 0 | 0.0 | 0.0 | exact | PASS | fresh:alg1_wide |  |
| 439 | alg-nodes | 0.25 | 0.25 | 0.25 | exact | PASS | fresh:alg1_wide |  |
| 439 | alg-nodes | 1.75 | 1.75 | 1.75 | exact | PASS | fresh:alg1_wide |  |
| 439 | alg-nodes-step | (statement) |  |  | conclusion | PASS | fresh:alg1_narrow,fresh:alg1_wide | nodes [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75] in both runs |
| 440 | alg-M | 2\times10^4 | 20000.0 | 20000.0 | exact | PASS | fresh:alg1_wide |  |
| 440 | alg-M | 0.01 | 0.01 | 0.01 | exact | PASS | fresh:alg1_wide |  |
| 440 | alg-M | 25 | 25.0 | 25.0 | exact | PASS | fresh:alg1_wide |  |
| 441 | alg-eps | 0.05 | 0.05 | 0.05 | exact | PASS | fresh:alg1_wide |  |
| 441 | alg-eps | 0.05 | 0.05 | 0.05 | exact | PASS | fresh:alg1_wide |  |
| 441 | alg-eps-formula | (statement) |  |  | conclusion | PASS | fresh:alg1_wide | eps = 0.5 sqrt(dt) bitwise |
| 441 | alg-gains | 0.3 | 0.3 | 0.3 | exact | PASS | fresh:alg1_wide |  |
| 441 | alg-gains | 1 | 1.0 | 1.0 | exact | PASS | fresh:alg1_wide |  |
| 441 | alg-gains | 10 | 10.0 | 10.0 | exact | PASS | fresh:alg1_wide |  |
| 441 | alg-gains | 0.1 | 0.1 | 0.1 | exact | PASS | fresh:alg1_wide |  |
| 441 | alg-gains | 0.15 | 0.15 | 0.15 | exact | PASS | fresh:alg1_wide |  |
| 441 | alg-gains | 3.5 | 3.5 | 3.5 | exact | PASS | fresh:alg1_wide |  |
| 441 | alg-gains | 60 | 60.0 | 60.0 | exact | PASS | fresh:alg1_wide |  |
| 443 | alg-params-same | two |  |  | conclusion | PASS | fresh:alg1_narrow,fresh:alg1_wide | two runs with identical parameters except the seed |
| 443 | alg-inits | 0.9 1 0.2 |  |  | conclusion | PASS | fresh:alg1_narrow,fresh:alg1_wide | initial boundaries in code and in the stored iteration 0 equal the printed formulas bitwise |
| 444 | alg-arms | two |  |  | conclusion | PASS |  | b1 and b2 receive separate updates (step1, step2) |
| 446 | alg-fall | 0.47 | 0.47 | 0.47219802177431297 | round | PASS | fresh:alg1_narrow,fresh:alg1_wide | third value: larger of the two runs at iteration 10 |
| 446 | alg-fall | 0.37 | 0.37 | 0.36788757483286805 | round | PASS | fresh:alg1_narrow,fresh:alg1_wide | third value: larger of the two runs at iteration 10 |
| 446 | alg-fall | 0.01 | 0.015359443598510632 | 0.015359443598510632 | about | APPROX | fresh:alg1_narrow,fresh:alg1_wide | third value: larger of the two runs at iteration 10 |
| 446 | alg-fd-N | 481 | 481.0 | 481.0 | exact | PASS | fresh:baseline481 |  |
| 447 | alg-fall-ten | ten |  |  | conclusion | PASS | fresh:alg1_narrow,fresh:alg1_wide | r.m.s. distance at iteration 10: wide 0.0154, narrow 0.0123 |
| 447 | alg-avg | 15 | 15.0 | 15.0 | exact | PASS | fresh:alg1_narrow,fresh:alg1_wide |  |
| 447 | alg-avg | 0.012 | 0.011537334135180544 | 0.011537334135180544 | le | PASS | fresh:alg1_narrow,fresh:alg1_wide |  |
| 448 | alg-agree-two | two |  |  | conclusion | PASS |  | wide and narrow |
| 449 | alg-agree | 0.01 | 0.007740228916358172 | 0.007740228916358172 | le | PASS | fresh:alg1_narrow,fresh:alg1_wide |  |
| 449 | alg-offset-sys | (statement) |  |  | conclusion | PASS | fresh:alg1_narrow,fresh:alg1_wide | r.m.s. error of averaged iterate vs mean of last iterates: [('0.0080', '0.0086'), ('0.0088', '0.0093')] |
| 450 | alg-offset | 0.01 | 0.01 | 0.01 | exact | PASS | fresh:alg1_wide |  |
| 452 | alg-loss | 3\times10^{-5} | 3e-5 | 2.9964792145033477e-05 | round | PASS | fresh:alg1_wide | wide run; the narrow run is checked in alg-loss-narrow |
| 452 | alg-loss | 2.6\times10^{-3} | 2.6e-3 | 0.0026032440536263354 | round | PASS | fresh:alg1_wide | wide run; the narrow run is checked in alg-loss-narrow |
| 452 | alg-loss-narrow | 3\times10^{-5} 2.6\times10^{-3} |  |  | conclusion | PASS | fresh:alg1_narrow | narrow run: mean 2.940e-05, max 2.603e-03 |
| 453 | alg-loss-where | (statement) |  |  | conclusion | PASS | fresh:alg1_narrow,fresh:alg1_wide,live:fd.Model(N=241).solve() | argmax of the loss at [('2.5000', '2.5000'), ('2.5000', '2.5000')] (last node s_n = 1.75); recomputed max equals stored max: [np.True_, np.True_] |
| 461 | fig-alg-two | two |  |  | conclusion | PASS | fresh:alg1_narrow,fresh:alg1_wide | max \|difference\| of averaged iterates 0.0077 |
| 469 | tab-alg-cap | 481 | 481.0 | 481.0 | exact | PASS | fresh:baseline481 |  |
| 469 | tab-alg-cap-two | two |  |  | conclusion | PASS |  | wide, narrow |
| 471 | tab-alg-se | 0.06 | 0.06 | 0.056590692442833566 | round | PASS | fresh:alg1_narrow,fresh:alg1_wide |  |
| 477 | tab-alg-wide | 0.472 | 0.472 | 0.47219802177431297 | round | PASS | fresh:alg1_wide |  |
| 477 | tab-alg-wide | 0.717 | 0.717 | 0.7165747171462395 | round | PASS | fresh:alg1_wide |  |
| 477 | tab-alg-wide | 3.54 | 3.54 | 3.540868966530181 | round | PASS | fresh:alg1_wide |  |
| 477 | tab-alg-wide | 5.0\times10^{-2} | 5e-2 | 0.05003347487571451 | round | PASS | fresh:alg1_wide |  |
| 477 | tab-alg-wide | 10 | 10.0 | 10.0 | exact | PASS | fresh:alg1_wide |  |
| 477 | tab-alg-wide | 0.015 | 0.015 | 0.015359443598510632 | round | PASS | fresh:alg1_wide |  |
| 477 | tab-alg-wide | 60 | 60.0 | 60.0 | exact | PASS | fresh:alg1_wide |  |
| 477 | tab-alg-wide | 0.008 | 0.008 | 0.00808574881163988 | round | PASS | fresh:alg1_wide |  |
| 477 | tab-alg-wide | 0.07 | 0.07 | 0.07340610213062967 | round | PASS | fresh:alg1_wide |  |
| 477 | tab-alg-wide | 15 | 15.0 | 15.0 | exact | PASS | fresh:alg1_wide |  |
| 477 | tab-alg-wide | 0.008 | 0.008 | 0.0080126964893886 | round | PASS | fresh:alg1_wide |  |
| 477 | tab-alg-wide | 0.011 | 0.011 | 0.011140165047851758 | round | PASS | fresh:alg1_wide |  |
| 477 | tab-alg-wide | 3.0\times10^{-5} | 3e-5 | 2.9964792145033477e-05 | round | PASS | fresh:alg1_wide |  |
| 482 | tab-alg-narrow | 0.368 | 0.368 | 0.36788757483286805 | round | PASS | fresh:alg1_narrow |  |
| 482 | tab-alg-narrow | 0.508 | 0.508 | 0.5082245501240483 | round | PASS | fresh:alg1_narrow |  |
| 482 | tab-alg-narrow | 1.10 | 1.10 | 1.1005790940034674 | round | PASS | fresh:alg1_narrow |  |
| 482 | tab-alg-narrow | 2.4\times10^{-2} | 2.4e-2 | 0.023500769738617328 | round | PASS | fresh:alg1_narrow |  |
| 482 | tab-alg-narrow | 10 | 10.0 | 10.0 | exact | PASS | fresh:alg1_narrow |  |
| 482 | tab-alg-narrow | 0.012 | 0.012 | 0.012301655879341733 | round | PASS | fresh:alg1_narrow |  |
| 482 | tab-alg-narrow | 60 | 60.0 | 60.0 | exact | PASS | fresh:alg1_narrow |  |
| 482 | tab-alg-narrow | 0.009 | 0.009 | 0.008547987835706745 | round | PASS | fresh:alg1_narrow |  |
| 482 | tab-alg-narrow | 0.07 | 0.07 | 0.06703000233080986 | round | PASS | fresh:alg1_narrow |  |
| 482 | tab-alg-narrow | 15 | 15.0 | 15.0 | exact | PASS | fresh:alg1_narrow |  |
| 482 | tab-alg-narrow | 0.009 | 0.009 | 0.008816859208983303 | round | PASS | fresh:alg1_narrow |  |
| 482 | tab-alg-narrow | 0.012 | 0.012 | 0.011537334135180544 | round | PASS | fresh:alg1_narrow |  |
| 482 | tab-alg-narrow | 2.9\times10^{-5} | 2.9e-5 | 2.9403159270511543e-05 | round | PASS | fresh:alg1_narrow |  |
| 491 | alg-two-starts | two |  |  | conclusion | PASS |  | 2 initialisations |
| 493 | alg-defect-level | (statement) |  |  | conclusion | PASS | fresh:alg1_narrow,fresh:alg1_wide | defect r.m.s. / standard error at the last iterate: ['1.32', '1.18'] |

## Every number token in the section

| line | token | status | verified by / reason |
|---|---|---|---|
| 14 | `1` | structural | index range of the coordinates |
| 14 | `2` | structural | index range of the coordinates |
| 14 | `1` | structural | index or exponent of a symbol |
| 14 | `2` | structural | index or exponent of a symbol |
| 16 | `0` | verified | kappa-positive |
| 17 | `0` | structural | index or exponent of a symbol |
| 17 | `1` | structural | index or exponent of a symbol |
| 17 | `1` | structural | index or exponent of a symbol |
| 17 | `2` | structural | index or exponent of a symbol |
| 17 | `2` | structural | index or exponent of a symbol |
| 17 | `1` | verified | rho-range |
| 18 | `1` | structural | growth exponent of Assumption ass:growth (theory input, not a computed value) |
| 19 | `1` | verified | q-formula |
| 19 | `2` | verified | q-formula |
| 19 | `2` | verified | q-formula |
| 19 | `1` | verified | q-formula |
| 19 | `2` | verified | q-formula |
| 19 | `2` | verified | q-formula |
| 19 | `2` | verified | q-formula |
| 19 | `2` | verified | q-formula |
| 20 | `-2` | verified | q-formula |
| 20 | `1` | verified | q-formula |
| 20 | `2` | verified | q-formula |
| 20 | `0` | verified | q-formula |
| 31 | `0.05` | verified | param-r |
| 32 | `1.0` | verified | param-alpha |
| 32 | `2` | structural | name of an exercise alternative |
| 33 | `1` | structural | index or exponent of a symbol |
| 33 | `2` | structural | index or exponent of a symbol |
| 33 | `0.4` | verified | param-kappa |
| 33 | `0.4` | verified | param-kappa |
| 34 | `1` | structural | index or exponent of a symbol |
| 34 | `2` | structural | index or exponent of a symbol |
| 34 | `1.0` | verified | param-theta |
| 34 | `1.0` | verified | param-theta |
| 35 | `1` | structural | index or exponent of a symbol |
| 35 | `2` | structural | index or exponent of a symbol |
| 35 | `0.4` | verified | param-sigma |
| 35 | `0.4` | verified | param-sigma |
| 36 | `0.0` | verified | param-rho |
| 37 | `0` | structural | index or exponent of a symbol |
| 37 | `1` | structural | index or exponent of a symbol |
| 37 | `2` | structural | index or exponent of a symbol |
| 37 | `0.01` | verified | param-c |
| 37 | `0` | verified | param-c |
| 37 | `0` | verified | param-c |
| 39 | `3` | verified | param-grid |
| 39 | `4` | verified | param-grid |
| 39 | `61` | verified | param-grid |
| 39 | `481` | verified | param-grid |
| 40 | `0` | verified | param-window |
| 40 | `2.5` | verified | param-window |
| 40 | `2` | structural | index or exponent of a symbol |
| 41 | `0.9` | verified | param-xref |
| 41 | `1.0` | verified | param-xref |
| 42 | `0.0025` | verified | param-mc |
| 42 | `0.02` | verified | param-mc |
| 42 | `40` | verified | param-mc |
| 42 | `2\times10^5` | verified | param-mc |
| 43 | `20261005` | verified | param-seed |
| 49 | `second` | verified | second-order |
| 50 | `12` | verified | monotone-correlated |
| 50 | `2` | verified | monotone-correlated |
| 50 | `1` | verified | monotone-correlated |
| 50 | `0` | verified | monotone-correlated |
| 51 | `seven` | verified | seven-point |
| 51 | `15` | verified | howard-iters |
| 51 | `28` | verified | howard-iters |
| 51 | `54` | verified | howard-iters |
| 51 | `107` | verified | howard-iters |
| 52 | `61` | verified | howard-iters |
| 52 | `121` | verified | howard-iters |
| 52 | `241` | verified | howard-iters |
| 52 | `481` | verified | howard-iters |
| 54 | `two` | verified | subcell-recon |
| 55 | `0` | verified | window-text |
| 55 | `2.5` | verified | window-text |
| 55 | `2` | structural | index or exponent of a symbol |
| 56 | `2` | verified | area-weight |
| 62 | `481` | verified | fig-N |
| 63 | `two` | verified | two-arms |
| 63 | `one` | verified | two-arms |
| 63 | `1` | structural | index or exponent of a symbol |
| 63 | `one` | verified | two-arms |
| 63 | `2` | structural | index or exponent of a symbol |
| 64 | `1` | structural | index or exponent of a symbol |
| 64 | `2` | structural | index or exponent of a symbol |
| 64 | `one` | structural | "one model": the study concerns a single benchmark |
| 67 | `one` | structural | "one-sided" is a name, not a quantity |
| 68 | `1` | verified | gac-threshold |
| 68 | `1` | verified | gac-threshold |
| 68 | `1` | verified | gac-threshold |
| 68 | `1` | verified | gac-threshold |
| 68 | `0` | verified | gac-threshold |
| 68 | `1` | verified | gac-threshold |
| 68 | `1` | verified | gac-threshold |
| 69 | `1` | structural | index or exponent of a symbol |
| 75 | `481` | verified | fig-regions-N |
| 75 | `1` | structural | index or exponent of a symbol |
| 75 | `2` | structural | index or exponent of a symbol |
| 76 | `0` | verified | fig-regions-gac0 |
| 77 | `half` | structural | "half-width" is a name |
| 77 | `4` | structural | constant of the formal expressions of Remark rem:width (values checked by claims) |
| 83 | `four` | verified | stable-digits |
| 83 | `0.01` | verified | bdry-within |
| 84 | `3` | verified | truncation |
| 84 | `4` | verified | truncation |
| 86 | `half` | structural | "half-width" is a name |
| 86 | `0.55` | verified | hw-text |
| 86 | `2` | structural | index or exponent of a symbol |
| 86 | `1` | verified | hw-text |
| 86 | `0.105` | verified | hw-text |
| 86 | `2` | structural | index or exponent of a symbol |
| 86 | `2.5` | verified | hw-text |
| 87 | `3` | verified | hw-formal-pct |
| 87 | `11` | verified | hw-formal-pct |
| 87 | `4` | structural | constant of the formal expressions of Remark rem:width (values checked by claims) |
| 87 | `2` | structural | index or exponent of a symbol |
| 88 | `2.5` | verified | premium-25 |
| 88 | `2.5` | verified | premium-25 |
| 88 | `0.0274` | verified | premium-25 |
| 88 | `16` | structural | constant of the formal expressions of Remark rem:width (values checked by claims) |
| 88 | `0.0272` | verified | premium-25 |
| 96 | `3` | verified | tab-refine-cap |
| 96 | `4` | verified | tab-refine-cap |
| 98 | `4` | structural | constant of the formal expressions of Remark rem:width (values checked by claims) |
| 101 | `half` | structural | "half-width" is a name |
| 101 | `1` | structural | index or exponent of a symbol |
| 101 | `2` | structural | index or exponent of a symbol |
| 101 | `2` | structural | index or exponent of a symbol |
| 101 | `2` | structural | index or exponent of a symbol |
| 103 | `1` | structural | index or exponent of a symbol |
| 103 | `0` | structural | symbol b1 at x2 = 0 (values checked by tab-refine-*) |
| 103 | `1.5` | verified | tab-refine-header |
| 103 | `2.0` | verified | tab-refine-header |
| 103 | `2.5` | verified | tab-refine-header |
| 105 | `61` | verified | tab-refine-61 |
| 105 | `0.05` | verified | tab-refine-61 |
| 105 | `0.27529` | verified | tab-refine-61 |
| 105 | `1.466` | verified | tab-refine-61 |
| 105 | `0.249` | verified | tab-refine-61 |
| 105 | `0.148` | verified | tab-refine-61 |
| 105 | `0.106` | verified | tab-refine-61 |
| 105 | `0.0500` | verified | tab-refine-61 |
| 106 | `121` | verified | tab-refine-121 |
| 106 | `0.025` | verified | tab-refine-121 |
| 106 | `0.27521` | verified | tab-refine-121 |
| 106 | `1.457` | verified | tab-refine-121 |
| 106 | `0.249` | verified | tab-refine-121 |
| 106 | `0.147` | verified | tab-refine-121 |
| 106 | `0.105` | verified | tab-refine-121 |
| 106 | `0.0250` | verified | tab-refine-121 |
| 107 | `241` | verified | tab-refine-241 |
| 107 | `0.0125` | verified | tab-refine-241 |
| 107 | `0.27519` | verified | tab-refine-241 |
| 107 | `1.463` | verified | tab-refine-241 |
| 107 | `0.249` | verified | tab-refine-241 |
| 107 | `0.147` | verified | tab-refine-241 |
| 107 | `0.104` | verified | tab-refine-241 |
| 107 | `0.0125` | verified | tab-refine-241 |
| 108 | `481` | verified | tab-refine-481 |
| 108 | `0.00625` | verified | tab-refine-481 |
| 108 | `0.27518` | verified | tab-refine-481 |
| 108 | `1.463` | verified | tab-refine-481 |
| 108 | `0.250` | verified | tab-refine-481 |
| 108 | `0.146` | verified | tab-refine-481 |
| 108 | `0.105` | verified | tab-refine-481 |
| 108 | `0.0063` | verified | tab-refine-481 |
| 110 | `4` | structural | constant of the formal expressions of Remark rem:width (values checked by claims) |
| 110 | `0.281` | verified | tab-refine-formal |
| 110 | `0.157` | verified | tab-refine-formal |
| 110 | `0.109` | verified | tab-refine-formal |
| 120 | `half` | structural | "half-width" is a name |
| 120 | `three` | verified | fig-refine-grids |
| 122 | `1` | structural | index or exponent of a symbol |
| 122 | `one` | verified | fig-refine-cell |
| 123 | `0` | verified | fig-refine-cell |
| 123 | `2.5` | verified | fig-refine-cell |
| 123 | `2` | structural | index or exponent of a symbol |
| 132 | `halves` | verified | sf-halves |
| 134 | `second` | verified | neumann-order |
| 141 | `first` | verified | tab-res-four |
| 141 | `four` | verified | tab-res-four |
| 145 | `121` | verified | tab-res-header |
| 145 | `241` | verified | tab-res-header |
| 145 | `481` | verified | tab-res-header |
| 147 | `0` | verified | tab-res-majorisation |
| 147 | `0` | verified | tab-res-majorisation |
| 147 | `0` | verified | tab-res-majorisation |
| 148 | `5\times10^{-13}` | verified | tab-res-superharmonic |
| 148 | `3\times10^{-12}` | verified | tab-res-superharmonic |
| 148 | `1\times10^{-11}` | verified | tab-res-superharmonic |
| 149 | `3\times10^{-13}` | verified | tab-res-complementarity |
| 149 | `1\times10^{-12}` | verified | tab-res-complementarity |
| 149 | `5\times10^{-12}` | verified | tab-res-complementarity |
| 150 | `6\times10^{-13}` | verified | tab-res-continuation_eq |
| 150 | `3\times10^{-12}` | verified | tab-res-continuation_eq |
| 150 | `1\times10^{-11}` | verified | tab-res-continuation_eq |
| 151 | `1` | structural | index or exponent of a symbol |
| 151 | `0.110` | verified | tab-res-smoothfit_max |
| 151 | `0.059` | verified | tab-res-smoothfit_max |
| 151 | `0.028` | verified | tab-res-smoothfit_max |
| 152 | `5.8\times10^{-4}` | verified | tab-res-neumann |
| 152 | `1.5\times10^{-4}` | verified | tab-res-neumann |
| 152 | `3.9\times10^{-5}` | verified | tab-res-neumann |
| 162 | `241` | verified | pol-N |
| 163 | `1.769` | verified | pol-meanV |
| 165 | `One` | structural | "one-sided" is a name, not a quantity |
| 165 | `2` | structural | index or exponent of a symbol |
| 166 | `1` | structural | index or exponent of a symbol |
| 166 | `one` | structural | "one particular policy" is not a quantity |
| 167 | `one` | structural | "one-sided" is a name, not a quantity |
| 167 | `one` | structural | "one-sided" is a name, not a quantity |
| 168 | `2` | structural | index or exponent of a symbol |
| 169 | `2` | structural | index or exponent of a symbol |
| 170 | `2` | structural | index or exponent of a symbol |
| 170 | `1` | structural | index or exponent of a symbol |
| 170 | `1` | structural | index or exponent of a symbol |
| 170 | `first` | verified | pol-firstrow |
| 171 | `1` | structural | name of an exercise alternative |
| 172 | `11.7` | verified | pol-ab-means |
| 172 | `13.6` | verified | pol-ab-means |
| 173 | `1` | structural | index or exponent of a symbol |
| 175 | `1` | structural | name of an exercise alternative |
| 175 | `one` | structural | "one-sided" is a name, not a quantity |
| 182 | `0` | verified | tab-loss-cap |
| 182 | `2.5` | verified | tab-loss-cap |
| 182 | `2` | structural | index or exponent of a symbol |
| 182 | `241` | verified | tab-loss-cap |
| 183 | `2` | structural | index or exponent of a symbol |
| 183 | `2` | structural | index or exponent of a symbol |
| 188 | `95` | verified | tab-loss-header |
| 188 | `95` | verified | tab-loss-header |
| 190 | `one` | structural | "one-sided" is a name, not a quantity |
| 190 | `13.61` | verified | tab-loss-one_retained |
| 190 | `40.91` | verified | tab-loss-one_retained |
| 190 | `47.10` | verified | tab-loss-one_retained |
| 190 | `0.390` | verified | tab-loss-one_retained |
| 190 | `1.345` | verified | tab-loss-one_retained |
| 190 | `1.649` | verified | tab-loss-one_retained |
| 191 | `one` | structural | "one-sided" is a name, not a quantity |
| 191 | `11.68` | verified | tab-loss-one_reopt |
| 191 | `38.65` | verified | tab-loss-one_reopt |
| 191 | `45.30` | verified | tab-loss-one_reopt |
| 191 | `0.338` | verified | tab-loss-one_reopt |
| 191 | `1.268` | verified | tab-loss-one_reopt |
| 191 | `1.585` | verified | tab-loss-one_reopt |
| 192 | `1.91` | verified | tab-loss-no_singular |
| 192 | `7.58` | verified | tab-loss-no_singular |
| 192 | `13.14` | verified | tab-loss-no_singular |
| 192 | `0.043` | verified | tab-loss-no_singular |
| 192 | `0.168` | verified | tab-loss-no_singular |
| 192 | `0.301` | verified | tab-loss-no_singular |
| 211 | `0` | structural | equation defining the stopping set of policy (c) |
| 213 | `0` | structural | index or exponent of a symbol |
| 216 | `0` | structural | equation defining the stopping set of policy (c) |
| 217 | `10^{-14}` | verified | gainform-check |
| 218 | `61` | verified | nosing-diag |
| 219 | `1` | structural | index or exponent of a symbol |
| 219 | `2` | structural | index or exponent of a symbol |
| 220 | `1.9` | verified | nosing-loss |
| 221 | `13.1` | verified | nosing-loss |
| 225 | `2` | structural | index or exponent of a symbol |
| 225 | `2` | structural | index or exponent of a symbol |
| 225 | `2` | structural | index or exponent of a symbol |
| 226 | `second` | structural | scheme property (checked by claim second-order) |
| 227 | `2` | verified | psi-formula |
| 227 | `2` | verified | psi-formula |
| 227 | `2` | verified | psi-formula |
| 227 | `2` | verified | psi-formula |
| 227 | `3` | verified | psi-formula |
| 227 | `2` | verified | psi-formula |
| 227 | `one` | verified | psi-formula |
| 228 | `0` | structural | index or exponent of a symbol |
| 229 | `2` | verified | smooth-bound |
| 230 | `2` | verified | smooth-bound |
| 237 | `2` | structural | index or exponent of a symbol |
| 237 | `2` | structural | index or exponent of a symbol |
| 237 | `2` | structural | index or exponent of a symbol |
| 238 | `241` | verified | tab-smooth-cap |
| 238 | `0` | verified | tab-smooth-cap |
| 238 | `2.5` | verified | tab-smooth-cap |
| 238 | `2` | verified | tab-smooth-cap |
| 238 | `0` | verified | tab-smooth-cap |
| 238 | `2` | verified | tab-smooth-cap |
| 246 | `0.8` | verified | tab-smooth-0.8 |
| 246 | `0.375` | verified | tab-smooth-0.8 |
| 246 | `6.32` | verified | tab-smooth-0.8 |
| 246 | `0.0088` | verified | tab-smooth-0.8 |
| 246 | `0.153` | verified | tab-smooth-0.8 |
| 246 | `0.49` | verified | tab-smooth-0.8 |
| 247 | `0.4` | verified | tab-smooth-0.4 |
| 247 | `0.109` | verified | tab-smooth-0.4 |
| 247 | `3.81` | verified | tab-smooth-0.4 |
| 247 | `0.0027` | verified | tab-smooth-0.4 |
| 247 | `0.097` | verified | tab-smooth-0.4 |
| 247 | `0.42` | verified | tab-smooth-0.4 |
| 248 | `0.2` | verified | tab-smooth-0.2 |
| 248 | `0.027` | verified | tab-smooth-0.2 |
| 248 | `1.85` | verified | tab-smooth-0.2 |
| 248 | `0.0008` | verified | tab-smooth-0.2 |
| 248 | `0.052` | verified | tab-smooth-0.2 |
| 248 | `0.30` | verified | tab-smooth-0.2 |
| 249 | `0.1` | verified | tab-smooth-0.1 |
| 249 | `0.003` | verified | tab-smooth-0.1 |
| 249 | `0.31` | verified | tab-smooth-0.1 |
| 249 | `0.0001` | verified | tab-smooth-0.1 |
| 249 | `0.011` | verified | tab-smooth-0.1 |
| 249 | `0` | verified | tab-smooth-0.1 |
| 250 | `0.05` | verified | tab-smooth-0.05 |
| 250 | `2\times10^{-4}` | verified | tab-smooth-0.05 |
| 250 | `0.017` | verified | tab-smooth-0.05 |
| 250 | `6\times10^{-6}` | verified | tab-smooth-0.05 |
| 250 | `6\times10^{-4}` | verified | tab-smooth-0.05 |
| 250 | `0` | verified | tab-smooth-0.05 |
| 251 | `0.025` | verified | tab-smooth-0.025 |
| 251 | `1\times10^{-5}` | verified | tab-smooth-0.025 |
| 251 | `0.003` | verified | tab-smooth-0.025 |
| 251 | `4\times10^{-7}` | verified | tab-smooth-0.025 |
| 251 | `9\times10^{-5}` | verified | tab-smooth-0.025 |
| 251 | `0` | verified | tab-smooth-0.025 |
| 267 | `0` | verified | bias-delta-enlarges |
| 268 | `-0.046` | verified | bias-text |
| 268 | `-0.022` | verified | bias-text |
| 269 | `-0.012` | verified | bias-text |
| 269 | `121` | verified | bias-text |
| 269 | `241` | verified | bias-text |
| 269 | `481` | verified | bias-text |
| 269 | `halves` | verified | bias-halves |
| 271 | `one` | verified | bias-order-one |
| 278 | `0` | structural | label of the unshifted row |
| 283 | `241` | verified | tab-bias-241--0.20 |
| 283 | `-0.20` | verified | tab-bias-241--0.20 |
| 283 | `-0.2266` | verified | tab-bias-241--0.20 |
| 283 | `-1.2683` | verified | tab-bias-241--0.20 |
| 283 | `-1.0417` | verified | tab-bias-241--0.20 |
| 284 | `241` | verified | tab-bias-241--0.10 |
| 284 | `-0.10` | verified | tab-bias-241--0.10 |
| 284 | `-0.2626` | verified | tab-bias-241--0.10 |
| 284 | `-0.7527` | verified | tab-bias-241--0.10 |
| 284 | `-0.4901` | verified | tab-bias-241--0.10 |
| 285 | `241` | verified | tab-bias-241--0.05 |
| 285 | `-0.05` | verified | tab-bias-241--0.05 |
| 285 | `-0.2723` | verified | tab-bias-241--0.05 |
| 285 | `-0.5064` | verified | tab-bias-241--0.05 |
| 285 | `-0.2341` | verified | tab-bias-241--0.05 |
| 286 | `241` | verified | tab-bias-241-0.05 |
| 286 | `0.05` | verified | tab-bias-241-0.05 |
| 286 | `-0.2703` | verified | tab-bias-241-0.05 |
| 286 | `-0.0598` | verified | tab-bias-241-0.05 |
| 286 | `0.2104` | verified | tab-bias-241-0.05 |
| 287 | `241` | verified | tab-bias-241-0.10 |
| 287 | `0.10` | verified | tab-bias-241-0.10 |
| 287 | `-0.2566` | verified | tab-bias-241-0.10 |
| 287 | `0.1358` | verified | tab-bias-241-0.10 |
| 287 | `0.3924` | verified | tab-bias-241-0.10 |
| 288 | `241` | verified | tab-bias-241-0.20 |
| 288 | `0.20` | verified | tab-bias-241-0.20 |
| 288 | `-0.1987` | verified | tab-bias-241-0.20 |
| 288 | `0.4664` | verified | tab-bias-241-0.20 |
| 288 | `0.6651` | verified | tab-bias-241-0.20 |
| 290 | `121` | verified | tab-bias-121-0 |
| 290 | `0` | verified | tab-bias-121-0 |
| 290 | `-0.2752` | verified | tab-bias-121-0 |
| 290 | `-0.3211` | verified | tab-bias-121-0 |
| 290 | `-0.0459` | verified | tab-bias-121-0 |
| 291 | `241` | verified | tab-bias-241-0 |
| 291 | `0` | verified | tab-bias-241-0 |
| 291 | `-0.2752` | verified | tab-bias-241-0 |
| 291 | `-0.2976` | verified | tab-bias-241-0 |
| 291 | `-0.0224` | verified | tab-bias-241-0 |
| 292 | `481` | verified | tab-bias-481-0 |
| 292 | `0` | verified | tab-bias-481-0 |
| 292 | `-0.2752` | verified | tab-bias-481-0 |
| 292 | `-0.2868` | verified | tab-bias-481-0 |
| 292 | `-0.0116` | verified | tab-bias-481-0 |
| 298 | `481` | verified | post-setup |
| 299 | `three` | structural | refers to E[Z], \|E[Z]\|, E\|Z\| (text) |
| 300 | `120` | verified | post-setup2 |
| 300 | `2\times10^4` | verified | post-setup2 |
| 301 | `0.005` | verified | post-setup2 |
| 303 | `0.0006` | verified | post-fine |
| 303 | `0.455` | verified | post-fine |
| 305 | `95` | verified | post-ci95 |
| 305 | `half` | structural | "half-width" is a name |
| 305 | `0.01` | verified | post-coarse |
| 306 | `0.0094` | verified | post-coarse |
| 306 | `0.445` | verified | post-coarse |
| 307 | `200` | verified | post-horizon |
| 307 | `0.01` | verified | post-horizon |
| 308 | `4\times10^{-4}` | verified | post-horizon |
| 308 | `2.5\times10^{-3}` | verified | post-discount |
| 308 | `120` | verified | post-discount |
| 310 | `one` | verified | post-order-one |
| 311 | `one` | structural | pronoun |
| 317 | `0` | structural | index or exponent of a symbol |
| 317 | `4` | verified | statics-grid |
| 317 | `321` | verified | statics-grid |
| 318 | `0.0125` | verified | statics-grid |
| 318 | `241` | verified | statics-grid |
| 319 | `0` | structural | index or exponent of a symbol |
| 321 | `0.576` | verified | statics-q-linear |
| 322 | `-0.8` | verified | statics-q-linear |
| 322 | `0.064` | verified | statics-q-linear |
| 322 | `0.8` | verified | statics-q-linear |
| 322 | `half` | structural | "half-width" is a name |
| 324 | `2` | verified | statics-premium-pct |
| 324 | `2` | verified | statics-premium-pct |
| 324 | `3` | verified | statics-premium-pct |
| 324 | `half` | structural | "half-width" is a name |
| 324 | `3` | verified | statics-hw-sym |
| 324 | `16` | verified | statics-hw-sym |
| 325 | `0.8` | verified | statics-two-cells |
| 325 | `two` | verified | statics-two-cells |
| 326 | `half` | structural | "half-width" is a name |
| 326 | `5` | verified | statics-asym |
| 326 | `12` | verified | statics-asym |
| 333 | `4` | verified | statics-cap |
| 333 | `321` | verified | statics-cap |
| 333 | `0.0125` | verified | statics-cap |
| 333 | `0` | verified | statics-cap |
| 333 | `2.5` | verified | statics-cap |
| 333 | `2` | structural | index or exponent of a symbol |
| 333 | `Half` | structural | "half-width" is a name |
| 334 | `1` | structural | index or exponent of a symbol |
| 334 | `2` | structural | index or exponent of a symbol |
| 335 | `1` | structural | index or exponent of a symbol |
| 335 | `2` | structural | index or exponent of a symbol |
| 335 | `2` | verified | statics-cap-G |
| 341 | `1` | structural | index or exponent of a symbol |
| 341 | `2` | structural | index or exponent of a symbol |
| 343 | `0.7` | verified | tab-statics-alpha-0.7 |
| 343 | `0.238` | verified | tab-statics-alpha-0.7 |
| 343 | `2.74` | verified | tab-statics-alpha-0.7 |
| 343 | `2.57` | verified | tab-statics-alpha-0.7 |
| 343 | `1.00` | verified | tab-statics-alpha-0.7 |
| 343 | `0.104` | verified | tab-statics-alpha-0.7 |
| 343 | `0.094` | verified | tab-statics-alpha-0.7 |
| 343 | `0.111` | verified | tab-statics-alpha-0.7 |
| 343 | `0.100` | verified | tab-statics-alpha-0.7 |
| 343 | `0.0243` | verified | tab-statics-alpha-0.7 |
| 344 | `1.0` | verified | tab-statics-alpha-1 |
| 344 | `0.320` | verified | tab-statics-alpha-1 |
| 344 | `2.66` | verified | tab-statics-alpha-1 |
| 344 | `1.83` | verified | tab-statics-alpha-1 |
| 344 | `1.83` | verified | tab-statics-alpha-1 |
| 344 | `0.147` | verified | tab-statics-alpha-1 |
| 344 | `0.147` | verified | tab-statics-alpha-1 |
| 344 | `0.157` | verified | tab-statics-alpha-1 |
| 344 | `0.157` | verified | tab-statics-alpha-1 |
| 344 | `0.0398` | verified | tab-statics-alpha-1 |
| 345 | `1.4` | verified | tab-statics-alpha-1.4 |
| 345 | `0.474` | verified | tab-statics-alpha-1.4 |
| 345 | `2.77` | verified | tab-statics-alpha-1.4 |
| 345 | `1.02` | verified | tab-statics-alpha-1.4 |
| 345 | `2.52` | verified | tab-statics-alpha-1.4 |
| 345 | `0.233` | verified | tab-statics-alpha-1.4 |
| 345 | `0.271` | verified | tab-statics-alpha-1.4 |
| 345 | `0.254` | verified | tab-statics-alpha-1.4 |
| 345 | `0.307` | verified | tab-statics-alpha-1.4 |
| 345 | `0.0735` | verified | tab-statics-alpha-1.4 |
| 346 | `0.03` | verified | tab-statics-r-0.03 |
| 346 | `0.320` | verified | tab-statics-r-0.03 |
| 346 | `3.00` | verified | tab-statics-r-0.03 |
| 346 | `1.65` | verified | tab-statics-r-0.03 |
| 346 | `1.65` | verified | tab-statics-r-0.03 |
| 346 | `0.159` | verified | tab-statics-r-0.03 |
| 346 | `0.159` | verified | tab-statics-r-0.03 |
| 346 | `0.170` | verified | tab-statics-r-0.03 |
| 346 | `0.170` | verified | tab-statics-r-0.03 |
| 346 | `0.0437` | verified | tab-statics-r-0.03 |
| 347 | `0.08` | verified | tab-statics-r-0.08 |
| 347 | `0.320` | verified | tab-statics-r-0.08 |
| 347 | `2.31` | verified | tab-statics-r-0.08 |
| 347 | `2.00` | verified | tab-statics-r-0.08 |
| 347 | `2.00` | verified | tab-statics-r-0.08 |
| 347 | `0.130` | verified | tab-statics-r-0.08 |
| 347 | `0.130` | verified | tab-statics-r-0.08 |
| 347 | `0.140` | verified | tab-statics-r-0.08 |
| 347 | `0.140` | verified | tab-statics-r-0.08 |
| 347 | `0.0353` | verified | tab-statics-r-0.08 |
| 348 | `0` | verified | tab-statics-c0-0.005 |
| 348 | `0.005` | verified | tab-statics-c0-0.005 |
| 348 | `0.320` | verified | tab-statics-c0-0.005 |
| 348 | `2.71` | verified | tab-statics-c0-0.005 |
| 348 | `1.80` | verified | tab-statics-c0-0.005 |
| 348 | `1.80` | verified | tab-statics-c0-0.005 |
| 348 | `0.148` | verified | tab-statics-c0-0.005 |
| 348 | `0.148` | verified | tab-statics-c0-0.005 |
| 348 | `0.158` | verified | tab-statics-c0-0.005 |
| 348 | `0.158` | verified | tab-statics-c0-0.005 |
| 348 | `0.0402` | verified | tab-statics-c0-0.005 |
| 349 | `0` | verified | tab-statics-c0-0.03 |
| 349 | `0.03` | verified | tab-statics-c0-0.03 |
| 349 | `0.320` | verified | tab-statics-c0-0.03 |
| 349 | `2.46` | verified | tab-statics-c0-0.03 |
| 349 | `1.92` | verified | tab-statics-c0-0.03 |
| 349 | `1.92` | verified | tab-statics-c0-0.03 |
| 349 | `0.141` | verified | tab-statics-c0-0.03 |
| 349 | `0.141` | verified | tab-statics-c0-0.03 |
| 349 | `0.151` | verified | tab-statics-c0-0.03 |
| 349 | `0.151` | verified | tab-statics-c0-0.03 |
| 349 | `0.0382` | verified | tab-statics-c0-0.03 |
| 350 | `-0.8` | verified | tab-statics-rho--0.8 |
| 350 | `0.576` | verified | tab-statics-rho--0.8 |
| 350 | `3.12` | verified | tab-statics-rho--0.8 |
| 350 | `1.60` | verified | tab-statics-rho--0.8 |
| 350 | `1.60` | verified | tab-statics-rho--0.8 |
| 350 | `0.250` | verified | tab-statics-rho--0.8 |
| 350 | `0.250` | verified | tab-statics-rho--0.8 |
| 350 | `0.282` | verified | tab-statics-rho--0.8 |
| 350 | `0.282` | verified | tab-statics-rho--0.8 |
| 350 | `0.0719` | verified | tab-statics-rho--0.8 |
| 351 | `-0.4` | verified | tab-statics-rho--0.4 |
| 351 | `0.448` | verified | tab-statics-rho--0.4 |
| 351 | `2.90` | verified | tab-statics-rho--0.4 |
| 351 | `1.71` | verified | tab-statics-rho--0.4 |
| 351 | `1.71` | verified | tab-statics-rho--0.4 |
| 351 | `0.200` | verified | tab-statics-rho--0.4 |
| 351 | `0.200` | verified | tab-statics-rho--0.4 |
| 351 | `0.220` | verified | tab-statics-rho--0.4 |
| 351 | `0.220` | verified | tab-statics-rho--0.4 |
| 351 | `0.0559` | verified | tab-statics-rho--0.4 |
| 352 | `0.4` | verified | tab-statics-rho-0.4 |
| 352 | `0.192` | verified | tab-statics-rho-0.4 |
| 352 | `2.39` | verified | tab-statics-rho-0.4 |
| 352 | `1.96` | verified | tab-statics-rho-0.4 |
| 352 | `1.96` | verified | tab-statics-rho-0.4 |
| 352 | `0.090` | verified | tab-statics-rho-0.4 |
| 352 | `0.090` | verified | tab-statics-rho-0.4 |
| 352 | `0.094` | verified | tab-statics-rho-0.4 |
| 352 | `0.094` | verified | tab-statics-rho-0.4 |
| 352 | `0.0237` | verified | tab-statics-rho-0.4 |
| 353 | `0.8` | verified | tab-statics-rho-0.8 |
| 353 | `0.064` | verified | tab-statics-rho-0.8 |
| 353 | `2.08` | verified | tab-statics-rho-0.8 |
| 353 | `2.12` | verified | tab-statics-rho-0.8 |
| 353 | `2.12` | verified | tab-statics-rho-0.8 |
| 353 | `0.026` | verified | tab-statics-rho-0.8 |
| 353 | `0.026` | verified | tab-statics-rho-0.8 |
| 353 | `0.031` | verified | tab-statics-rho-0.8 |
| 353 | `0.031` | verified | tab-statics-rho-0.8 |
| 353 | `0.0076` | verified | tab-statics-rho-0.8 |
| 363 | `-0.8` | verified | fig-rho-cap |
| 363 | `-0.6` | verified | fig-rho-cap |
| 363 | `0.8` | verified | fig-rho-cap |
| 363 | `0.0125` | verified | fig-rho-cap |
| 363 | `half` | structural | "half-width" is a name |
| 364 | `2` | verified | fig-rho-pts |
| 364 | `2` | verified | fig-rho-pts |
| 364 | `4` | structural | constant of the formal expressions of Remark rem:width (values checked by claims) |
| 365 | `2` | verified | fig-rho-pts |
| 365 | `2` | verified | fig-rho-pts |
| 365 | `16` | structural | constant of the formal expressions of Remark rem:width (values checked by claims) |
| 373 | `0.9` | verified | mc-xref |
| 373 | `1.0` | verified | mc-xref |
| 374 | `481` | verified | mc-xref |
| 375 | `-0.2752` | verified | mc-P |
| 375 | `0` | structural | index or exponent of a symbol |
| 375 | `0.1` | verified | mc-Y0 |
| 376 | `2\times10^5` | verified | mc-M |
| 376 | `40` | verified | mc-M |
| 377 | `3.6` | verified | mc-tau |
| 377 | `3.9` | verified | mc-tau |
| 378 | `5\times10^{-5}` | verified | mc-alive |
| 379 | `0.135` | verified | mc-disc |
| 384 | `95` | verified | mc-cap |
| 384 | `half` | structural | "half-width" is a name |
| 385 | `2\times10^5` | verified | mc-cap |
| 385 | `-0.2752` | verified | mc-cap |
| 392 | `2` | verified | mc-header |
| 392 | `0.4` | verified | mc-header |
| 394 | `0.02` | verified | tab-mc-0.02 |
| 394 | `-0.2735` | verified | tab-mc-0.02 |
| 394 | `-0.2687` | verified | tab-mc-0.02 |
| 394 | `-0.2711` | verified | tab-mc-0.02 |
| 394 | `-0.2307` | verified | tab-mc-0.02 |
| 394 | `-0.2531` | verified | tab-mc-0.02 |
| 394 | `0.0024` | verified | tab-mc-0.02 |
| 395 | `0.01` | verified | tab-mc-0.01 |
| 395 | `-0.2742` | verified | tab-mc-0.01 |
| 395 | `-0.2723` | verified | tab-mc-0.01 |
| 395 | `-0.2770` | verified | tab-mc-0.01 |
| 395 | `-0.2549` | verified | tab-mc-0.01 |
| 395 | `-0.2652` | verified | tab-mc-0.01 |
| 395 | `-0.0028` | verified | tab-mc-0.01 |
| 396 | `0.005` | verified | tab-mc-0.005 |
| 396 | `-0.2754` | verified | tab-mc-0.005 |
| 396 | `-0.2732` | verified | tab-mc-0.005 |
| 396 | `-0.2722` | verified | tab-mc-0.005 |
| 396 | `-0.2678` | verified | tab-mc-0.005 |
| 396 | `-0.2715` | verified | tab-mc-0.005 |
| 396 | `0.0032` | verified | tab-mc-0.005 |
| 397 | `0.0025` | verified | tab-mc-0.0025 |
| 397 | `-0.2754` | verified | tab-mc-0.0025 |
| 397 | `-0.2744` | verified | tab-mc-0.0025 |
| 397 | `-0.2740` | verified | tab-mc-0.0025 |
| 397 | `-0.2742` | verified | tab-mc-0.0025 |
| 397 | `-0.2727` | verified | tab-mc-0.0025 |
| 397 | `0.0015` | verified | tab-mc-0.0025 |
| 402 | `half` | structural | "half-width" is a name |
| 410 | `four` | verified | fig-mc-cap |
| 411 | `2\times10^5` | verified | fig-mc-cap |
| 412 | `0` | structural | index or exponent of a symbol |
| 412 | `0.005` | verified | fig-mc-cap2 |
| 413 | `95` | verified | fig-mc-cap2 |
| 417 | `Three` | verified | mc-three |
| 417 | `First` | structural | text structure (enumeration) |
| 418 | `-0.2754` | verified | mc-direct |
| 419 | `0.002` | verified | mc-direct-bias |
| 419 | `0.02` | verified | mc-direct-bias |
| 419 | `Second` | structural | text structure (enumeration) |
| 419 | `0` | structural | index or exponent of a symbol |
| 419 | `0.1` | verified | mc-paired |
| 419 | `one` | structural | pronoun |
| 420 | `0.005` | verified | mc-paired |
| 420 | `one` | verified | mc-paired |
| 420 | `two` | verified | mc-paired |
| 420 | `half` | structural | "half-width" is a name |
| 421 | `0.01` | verified | mc-spread |
| 421 | `0.05` | verified | mc-spread |
| 421 | `0.1` | verified | mc-spread |
| 421 | `0.2` | verified | mc-spread |
| 422 | `-0.2723` | verified | mc-spread |
| 422 | `-0.2770` | verified | mc-spread |
| 422 | `-0.2549` | verified | mc-spread |
| 422 | `0.022` | verified | mc-spread |
| 422 | `ten` | verified | mc-spread-ten |
| 423 | `half` | structural | "half-width" is a name |
| 427 | `0.4` | verified | mc-third |
| 433 | `half` | verified | mc-scaling |
| 433 | `-1` | verified | mc-scaling |
| 433 | `2` | verified | mc-scaling |
| 439 | `0` | verified | alg-nodes |
| 439 | `0.25` | verified | alg-nodes |
| 439 | `1.75` | verified | alg-nodes |
| 440 | `2\times10^4` | verified | alg-M |
| 440 | `0.01` | verified | alg-M |
| 440 | `25` | verified | alg-M |
| 441 | `0.05` | verified | alg-eps |
| 441 | `0.05` | verified | alg-eps |
| 442 | `0.3` | verified | alg-gains |
| 442 | `1` | verified | alg-gains |
| 442 | `10` | verified | alg-gains |
| 442 | `0.15` | verified | alg-gains |
| 443 | `3.5` | verified | alg-gains |
| 443 | `60` | verified | alg-gains |
| 443 | `two` | verified | alg-params-same |
| 443 | `one` | verified | alg-inits |
| 444 | `1` | verified | alg-inits |
| 444 | `2` | verified | alg-inits |
| 444 | `0.9` | verified | alg-inits |
| 444 | `one` | verified | alg-inits |
| 444 | `1` | verified | alg-inits |
| 444 | `2` | verified | alg-inits |
| 444 | `1` | verified | alg-inits |
| 444 | `0.2` | verified | alg-inits |
| 444 | `two` | verified | alg-arms |
| 446 | `481` | verified | alg-fd-N |
| 447 | `0.47` | verified | alg-fall |
| 447 | `0.37` | verified | alg-fall |
| 447 | `0.01` | verified | alg-fall |
| 447 | `ten` | verified | alg-fall |
| 448 | `15` | verified | alg-avg |
| 448 | `0.012` | verified | alg-avg |
| 449 | `two` | verified | alg-agree-two |
| 449 | `0.01` | verified | alg-agree |
| 450 | `0.01` | verified | alg-offset |
| 453 | `3\times10^{-5}` | verified | alg-loss |
| 453 | `2.6\times10^{-3}` | verified | alg-loss |
| 461 | `two` | verified | fig-alg-two |
| 469 | `two` | verified | tab-alg-cap |
| 470 | `481` | verified | tab-alg-cap |
| 471 | `0.06` | verified | tab-alg-se |
| 477 | `0.472` | verified | tab-alg-wide |
| 477 | `0.717` | verified | tab-alg-wide |
| 477 | `3.54` | verified | tab-alg-wide |
| 477 | `5.0\times10^{-2}` | verified | tab-alg-wide |
| 478 | `10` | verified | tab-alg-wide |
| 478 | `0.015` | verified | tab-alg-wide |
| 479 | `60` | verified | tab-alg-wide |
| 479 | `0.008` | verified | tab-alg-wide |
| 479 | `0.07` | verified | tab-alg-wide |
| 480 | `15` | verified | tab-alg-wide |
| 480 | `0.008` | verified | tab-alg-wide |
| 480 | `0.011` | verified | tab-alg-wide |
| 480 | `3.0\times10^{-5}` | verified | tab-alg-wide |
| 482 | `0.368` | verified | tab-alg-narrow |
| 482 | `0.508` | verified | tab-alg-narrow |
| 482 | `1.10` | verified | tab-alg-narrow |
| 482 | `2.4\times10^{-2}` | verified | tab-alg-narrow |
| 483 | `10` | verified | tab-alg-narrow |
| 483 | `0.012` | verified | tab-alg-narrow |
| 484 | `60` | verified | tab-alg-narrow |
| 484 | `0.009` | verified | tab-alg-narrow |
| 484 | `0.07` | verified | tab-alg-narrow |
| 485 | `15` | verified | tab-alg-narrow |
| 485 | `0.009` | verified | tab-alg-narrow |
| 485 | `0.012` | verified | tab-alg-narrow |
| 485 | `2.9\times10^{-5}` | verified | tab-alg-narrow |
| 491 | `two` | verified | alg-two-starts |
