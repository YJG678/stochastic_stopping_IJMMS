"""Negative controls: alter printed numbers in a copy of the section and confirm that the
verifier reports each alteration as a failure. Run:  python3 -m verify.selftest SECTION.tex"""
import sys, os, tempfile, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from verify import engine
from verify.claims_numerics import CLAIMS, STRUCTURAL

# (original text, altered text, what is altered)
MUTATIONS = [
    ('$0.27521$', '$0.27522$', 'last digit of a table value'),
    ('$13.61$', '$13.62$', 'last digit of a percentage'),
    ('$5\\times10^{-13}$', '$4\\times10^{-13}$', 'mantissa of a round-off residual'),
    ('$-0.2735\\pm0.0011$', '$-0.2735\\pm0.0012$', 'confidence half-width'),
    ('$r$ & $0.05$', '$r$ & $0.050001$', 'model parameter'),
    ('steps for $N=61,121,241,481$', 'steps for $N=61,121,241,482$', 'grid size'),
    ('more than ten times', 'more than twenty times', 'number word in a conclusion'),
    ('by at most\n$0.005$', 'by at most\n$0.004$', 'bound in a conclusion'),
    ('falls\nfrom $0.47$', 'falls\nfrom $0.48$', 'iteration history'),
    ('$0.0094\\pm0.0079$', '$0.0094\\pm0.0080$', 'Monte Carlo half-width'),
    ('reproduces $\\hat V_{\\rm ref}-G$ to $10^{-14}$', 'reproduces $\\hat V_{\\rm ref}-G$ to $10^{-15}$', 'order of magnitude'),
    ('within $3$--$11\\%$', 'within $3$--$12\\%$', 'range in the text'),
    ('the wedge spans only about two cells', 'the wedge spans only about three cells', 'number word'),
    ('$0.0743$', '$0.0743$', None),  # placeholder, skipped if absent
]


def run(path):
    text0 = open(path).read()
    ctx = engine.Context(None, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'results'))
    t, mk = engine.load_source(path)
    base_rows, _ = engine.evaluate(CLAIMS, t, mk, ctx)
    base_fail = {(r['id'], r['printed']) for r in base_rows if r['status'] == 'FAIL'}
    ok_all = True
    for old, new, what in MUTATIONS:
        if what is None or old not in text0:
            continue
        txt = text0.replace(old, new, 1)
        with tempfile.NamedTemporaryFile('w', suffix='.tex', delete=False) as f:
            f.write(txt); p = f.name
        t, mk = engine.load_source(p)
        rows, covered = engine.evaluate(CLAIMS, t, mk, ctx)
        cov = engine.coverage(t, mk, covered, STRUCTURAL)
        new_fail = [r for r in rows if r['status'] == 'FAIL' and (r['id'], r['printed']) not in base_fail]
        unacc = [c for c in cov if c['status'] == 'UNACCOUNTED']
        detected = bool(new_fail or unacc)
        ok_all &= detected
        print('%-9s %-40s -> %s' % ('DETECTED' if detected else 'MISSED', what,
                                    ', '.join(sorted({r['id'] for r in new_fail})) or ('unaccounted: ' + ', '.join(c['token'] for c in unacc))))
        os.unlink(p)
    print('all alterations detected' if ok_all else 'SOME ALTERATIONS WERE NOT DETECTED')
    return ok_all


if __name__ == '__main__':
    sys.exit(0 if run(sys.argv[1]) else 1)
