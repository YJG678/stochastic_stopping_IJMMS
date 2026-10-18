"""Re-execute the experiment scripts into a fresh directory and compare their output with
the stored results, value by value, in units in the last place (ULP)."""
import os, sys, json, subprocess, time
import numpy as np
from .texnum import ulp_distance

CODE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (script, arguments, files written)
FD_JOBS = [('ex1d.py', [], ['ex1d.json']),
           ('exp_fd.py', ['e1', 'e2', 'e3', 'e3c', 'e4'],
            ['e1_refinement.json', 'baseline481.npz', 'e2_residuals.json', 'e3_policies.json', 'e3_maps.npz',
             'e3c_bias.json', 'e4_statics.json'])]
MC_JOBS = [('exp_mc.py', ['e5', 'e5post'], ['e5_mc.json', 'e5_mc_M.json', 'e5_post.json']),
           ('alg1.py', ['wide'], ['alg1_wide.json']),
           ('alg1.py', ['narrow'], ['alg1_narrow.json'])]


def run_jobs(jobs, outdir, log):
    os.makedirs(outdir, exist_ok=True)
    env = dict(os.environ, NUMERICS_RESULTS=outdir, PYTHONHASHSEED='0')
    for script, args, _ in jobs:
        t = time.time()
        log('  running %s %s ...' % (script, ' '.join(args)))
        r = subprocess.run([sys.executable, os.path.join(CODE, script)] + args, cwd=CODE, env=env,
                           capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError('%s failed:\n%s' % (script, r.stderr[-3000:]))
        log('    done in %.0f s' % (time.time() - t))


def _flatten(x, path=''):
    if isinstance(x, dict):
        for k in sorted(x):
            yield from _flatten(x[k], path + '/' + str(k))
    elif isinstance(x, (list, tuple)):
        for i, v in enumerate(x):
            yield from _flatten(v, path + '[%d]' % i)
    else:
        yield path, x


def compare_file(fname, stored_dir, fresh_dir):
    a_p, b_p = os.path.join(stored_dir, fname), os.path.join(fresh_dir, fname)
    worst, n, where, mismatch = 0.0, 0, '', []
    if fname.endswith('.json'):
        A = dict(_flatten(json.load(open(a_p)))); Bv = dict(_flatten(json.load(open(b_p))))
        assert set(A) == set(Bv), 'different structure in %s' % fname
        for k in A:
            a, b = A[k], Bv[k]
            if isinstance(a, bool) or isinstance(a, str) or a is None:
                if a != b: mismatch.append(k)
                continue
            u = ulp_distance(a, b); n += 1
            if u > worst: worst, where = u, k
    else:
        A, Bv = np.load(a_p), np.load(b_p)
        assert set(A.files) == set(Bv.files)
        for k in A.files:
            a, b = A[k].ravel(), Bv[k].ravel()
            if a.dtype == bool:
                if not np.array_equal(a, b): mismatch.append(k)
                n += a.size; continue
            a = a.astype(float); b = b.astype(float)
            same = (a == b) | (np.isnan(a) & np.isnan(b))
            n += a.size
            if not same.all():
                d = np.abs(a - b)[~same] / np.spacing(np.maximum(np.abs(a), np.abs(b))[~same])
                if d.max() > worst: worst, where = float(d.max()), k
    return dict(file=fname, n=n, max_ulp=('%.3g' % worst) + (' (%s)' % where if where else ''),
                ulp=worst, identical=(worst == 0 and not mismatch), mismatch=mismatch)
