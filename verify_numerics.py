#!/usr/bin/env python3
"""Verify every number reported in the section "Numerical study" against the code.

Usage
  python3 verify_numerics.py SECTION.tex [--mode quick|full|stored] [--report report.md] [--max-ulp K]

What is checked
  1. Re-execution. The experiment scripts are run again into a fresh directory
     (mode quick: the deterministic finite-difference experiments, about 3 minutes;
      mode full: additionally the Monte Carlo experiments and both runs of Algorithm 1,
      about one hour; mode stored: nothing is re-run). Every value of the fresh output is
     compared with the stored results in units in the last place; identical seeds and
     libraries must give bitwise-identical output, and any difference larger than --max-ulp
     (default 0) is reported as a failure.
  2. Every printed number. Each number in the section is located by a verbatim quotation
     (verify/claims_numerics.py) and recomputed from the code output. A rounded number passes
     only if the exact binary value of the computed double, rounded half-up to the printed
     number of decimals or significant digits, is identical to the printed decimal; inputs of
     the code (parameters, grid sizes, seeds) must equal the configured double bitwise; bounds
     ("below", "at most", "within") are checked as inequalities.
  3. Every conclusion that rests on the numbers ("halves with h", "two arms", "more than ten
     times the half-width", ...) is re-evaluated with a criterion stated in the report.
  4. Coverage. Every number token and number word in the section must be verified by a claim
     or classified as structural (an index, a formula constant, a label) with a stated reason.
     Unaccounted numbers make the verification fail.

Exit status 0 if everything passes, 1 otherwise. A Markdown report lists every check.
"""
import argparse, os, sys, json, time, tempfile, shutil, platform

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ.setdefault('NUMERICS_RESULTS', os.path.join(HERE, 'results'))

from verify import engine, reproduce
from verify.claims_numerics import CLAIMS, STRUCTURAL


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('section', help='LaTeX source of the numerical section')
    ap.add_argument('--mode', choices=['stored', 'quick', 'full'], default='quick')
    ap.add_argument('--report', default=os.path.join(HERE, 'verification_report.md'))
    ap.add_argument('--fresh-dir', default=None, help='directory for re-executed output (default: temporary)')
    ap.add_argument('--reuse', action='store_true',
                    help='do not execute; compare the files already present in --fresh-dir')
    ap.add_argument('--max-ulp', type=float, default=0.0,
                    help='largest accepted ULP distance between stored and re-executed output (default 0 = bitwise)')
    a = ap.parse_args()
    log = lambda s: print(s, flush=True)
    stored = os.path.join(HERE, 'results')
    fresh = None
    repro = []
    t0 = time.time()
    if a.mode != 'stored':
        fresh = a.fresh_dir or tempfile.mkdtemp(prefix='numerics_fresh_')
        jobs = reproduce.FD_JOBS + (reproduce.MC_JOBS if a.mode == 'full' else [])
        if a.reuse:
            log('Using existing re-executed output in %s' % fresh)
        else:
            log('Re-executing %d job(s) into %s' % (len(jobs), fresh))
            reproduce.run_jobs(jobs, fresh, log)
        for _, _, files in jobs:
            for f in files:
                r = reproduce.compare_file(f, stored, fresh)
                r['identical'] = r['identical'] or (r['ulp'] <= a.max_ulp and not r['mismatch'])
                repro.append(r)
                log('  %-22s %7d values  max ULP distance %s' % (f, r['n'], r['max_ulp']))
    log('Checking %d claims against the paper ...' % len(CLAIMS))
    text, masked = engine.load_source(a.section)
    ctx = engine.Context(fresh, stored)
    rows, covered = engine.evaluate(CLAIMS, text, masked, ctx)
    cov = engine.coverage(text, masked, covered, STRUCTURAL)
    import numpy, scipy
    meta = {'section': os.path.abspath(a.section), 'mode': a.mode,
            're-executed now': ', '.join(f for _, _, fs in (reproduce.FD_JOBS + (reproduce.MC_JOBS if a.mode == 'full' else [])) for f in fs) if fresh else 'nothing (stored output only)',
            'taken from stored output': 'none' if a.mode == 'full' else ('Monte Carlo and Algorithm 1 results (rerun with --mode full)' if a.mode == 'quick' else 'all'),
            'comparison rule': 'printed decimals: exact binary value of the double rounded half-up to the printed precision must equal the printed decimal; inputs: bitwise equality',
            'platform': '%s, Python %s, NumPy %s, SciPy %s' % (platform.platform(), platform.python_version(), numpy.__version__, scipy.__version__),
            'run time': '%.0f s' % (time.time() - t0)}
    n, un = engine.write_report(a.report, rows, cov, repro, meta)
    bad_repro = [r for r in repro if not r['identical']]
    log('\nResult: %d passed, %d approximate, %d FAILED; %d number tokens, %d unaccounted; %d of %d re-executed files bitwise identical'
        % (n['PASS'], n['APPROX'], n['FAIL'], len(cov), len(un), len(repro) - len(bad_repro), len(repro)))
    for r in rows:
        if r['status'] == 'FAIL':
            log('  FAIL line %s %-24s printed %-12s code %-14s %s' % (r['line'], r['id'], r['printed'], r['computed'] or r['full'], r['detail']))
    for c in un:
        log('  UNACCOUNTED line %s: %s' % (c['line'], c['token']))
    log('Report written to %s' % a.report)
    if fresh and not a.fresh_dir:
        shutil.rmtree(fresh, ignore_errors=True)
    sys.exit(0 if (n['FAIL'] == 0 and not un and not bad_repro) else 1)


if __name__ == '__main__':
    main()
