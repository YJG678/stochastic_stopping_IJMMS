#!/bin/sh
# Regenerates every number, table entry and figure of the numerical section.
# Total run time on a 2-core machine: roughly 45-60 minutes (the two alg1 runs dominate).
set -e
python3 ex1d.py   # closed-form example
python3 exp_fd.py e1 e2 e3 e3c e4    # finite-difference experiments 
python3 exp_mc.py e5 e5post          # Monte Carlo estimator study, post-stopping functional 
python3 alg1.py wide                 # Algorithm 1, wide initial boundary   
python3 alg1.py narrow               # Algorithm 1, narrow initial boundary
python3 figs.py                      # all figures -> ../paper/figs
