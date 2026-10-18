"""Matching of claims against the LaTeX source, evaluation, coverage and reporting."""
import re, json, os, math
import numpy as np
from .texnum import Printed, NUM, NUM_RE, WORD_RE, WORDS

# ----------------------------------------------------------------------------- claims
class Claim:
    """A located statement in the paper.

    snippet : literal LaTeX text as it appears in the paper; '@' marks a printed number,
              '@w' a number word ('ten', 'two', ...). Whitespace in the snippet matches any
              whitespace (including line breaks).
    values  : callable(ctx) -> list of computed values, one per '@' (optional)
    rules   : rule for each '@' (or one rule for all): 'round' (exact at printed precision),
              'exact' (bitwise equality with a configured input), 'le', 'lt', 'ge', 'gt'
              (printed number is a bound), 'about' (within one unit of the last printed
              digit; reported separately as APPROX)
    check   : callable(ctx, printed_list) -> (ok, detail) for conclusions and statements
              that are not a single rounded number (optional)
    """

    def __init__(self, cid, snippet, values=None, rules='round', check=None, note=''):
        self.id, self.snippet, self.values, self.rules, self.check, self.note = cid, snippet, values, rules, check, note


def compile_snippet(snippet):
    parts = re.split(r'(@w|@|\s+)', snippet)
    out, kinds = [], []
    for p in parts:
        if p == '@':
            out.append('(' + NUM + ')'); kinds.append('num')
        elif p == '@w':
            out.append(r'(\b[A-Za-z]+\b)'); kinds.append('word')
        elif p and p.isspace():
            out.append(r'\s+')
        elif p:
            out.append(re.escape(p))
    return re.compile(''.join(out)), kinds


# ----------------------------------------------------------------------------- context
class Context:
    """Access to code output. FD results come from `fresh` (re-executed now) when available,
    otherwise from `stored`; every access is recorded so that each claim reports its provenance."""

    def __init__(self, fresh_dir, stored_dir):
        self.fresh, self.stored = fresh_dir, stored_dir
        self.cache, self.used = {}, set()

    def _path(self, fname):
        if self.fresh and os.path.exists(os.path.join(self.fresh, fname)):
            return os.path.join(self.fresh, fname), 'fresh'
        return os.path.join(self.stored, fname), 'stored'

    def json(self, name):
        p, tag = self._path(name + '.json'); self.used.add('%s:%s' % (tag, name))
        if p not in self.cache:
            with open(p) as f:
                self.cache[p] = json.load(f)
        return self.cache[p]

    def npz(self, name):
        p, tag = self._path(name + '.npz'); self.used.add('%s:%s' % (tag, name))
        if p not in self.cache:
            self.cache[p] = dict(np.load(p))
        return self.cache[p]

    def live(self, what):
        self.used.add('live:' + what)


# ----------------------------------------------------------------------------- source text
MARKUP = [r'\\(?:label|ref|cref|Cref|eqref|includegraphics|cite)\*?(?:\[[^\]]*\])?\{[^}]*\}',
          r'\\begin\{rv\}\{[^}]*\}\{(?:[^{}]|\{[^{}]*\})*\}',
          r'\\(?:begin|end)\{[a-z*]+\}(?:\[[^\]]*\])?',
          r'\\begin\{tabular\}\{[^}]*\}', r'\\cmidrule\([^)]*\)\{[^}]*\}', r'\\multicolumn\{\d+\}\{[^}]*\}',
          r'\\(?:tE|tA|tB)\{[^}]*\}']


def load_source(path):
    raw = open(path).read()
    # strip comments, keeping offsets
    text = re.sub(r'(?<!\\)%[^\n]*', lambda m: ' ' * len(m.group(0)), raw)
    masked = [False] * len(text)
    for rx in MARKUP:
        for m in re.finditer(rx, text):
            for i in range(m.start(), m.end()):
                masked[i] = True
    return text, masked


def line_of(text, pos):
    return text.count('\n', 0, pos) + 1


def tokens(text, masked):
    out = []
    for m in NUM_RE.finditer(text):
        if not masked[m.start()]:
            out.append(('num', m.start(), m.end(), m.group(0)))
    for m in WORD_RE.finditer(text):
        if not masked[m.start()]:
            out.append(('word', m.start(), m.end(), m.group(0)))
    return sorted(out, key=lambda t: t[1])


# ----------------------------------------------------------------------------- evaluation
def _rule_ok(rule, p, x):
    if rule == 'round':
        return ('PASS' if p.matches(x) else 'FAIL'), p.fmt(x)
    if rule == 'exact':
        return ('PASS' if float(x) == p.float else 'FAIL'), repr(float(x))
    if rule in ('le', 'lt', 'ge', 'gt'):
        ok = {'le': x <= p.float, 'lt': x < p.float, 'ge': x >= p.float, 'gt': x > p.float}[rule]
        return ('PASS' if ok else 'FAIL'), repr(float(x))
    if rule == 'about':
        ok = abs(float(x) - p.float) <= float(p.unit()) * (1 + 1e-12)
        return ('APPROX' if ok else 'FAIL'), repr(float(x))
    raise ValueError(rule)


def evaluate(claims, text, masked, ctx):
    rows, covered, problems = [], [], []
    for c in claims:
        rx, kinds = compile_snippet(c.snippet)
        ms = [m for m in rx.finditer(text)]
        if len(ms) != 1:
            problems.append(dict(id=c.id, status='FAIL', line='-', printed='-', computed='-', full='-', rule='-', src='',
                                 detail='snippet %s in the paper (%d matches): %s' %
                                 ('not found' if not ms else 'ambiguous', len(ms), c.snippet[:70])))
            continue
        m = ms[0]
        line = line_of(text, m.start())
        for g in range(1, len(kinds) + 1):
            covered.append((m.start(g), m.end(g), c.id))
        if getattr(c, 'covers', False) or getattr(c, 'covers_first', False):
            covered.append((m.start(), m.end(), c.id))
        nums = [Printed(m.group(g + 1)) for g, k in enumerate(kinds) if k == 'num']
        words = [m.group(g + 1) for g, k in enumerate(kinds) if k == 'word']
        ctx.used = set()
        try:
            if c.values is not None:
                vals = c.values(ctx)
                assert len(vals) == len(nums), 'claim %s: %d values for %d printed numbers' % (c.id, len(vals), len(nums))
                rules = c.rules if isinstance(c.rules, (list, tuple)) else [c.rules] * len(nums)
                for p, x, r in zip(nums, vals, rules):
                    st, comp = _rule_ok(r, p, x)
                    rows.append(dict(id=c.id, line=line, printed=p.s, computed=comp, full=repr(float(x)),
                                     rule=r, status=st, src=','.join(sorted(ctx.used)), detail=c.note))
            if c.check is not None:
                ok, detail = c.check(ctx, nums + words)
                rows.append(dict(id=c.id, line=line, printed=' '.join([p.s for p in nums] + words) or '(statement)',
                                 computed='', full='', rule='conclusion', status='PASS' if ok else 'FAIL',
                                 src=','.join(sorted(ctx.used)), detail=detail))
        except Exception as e:  # a crash in a claim is a failure, never a silent pass
            rows.append(dict(id=c.id, line=line, printed='', computed='', full='', rule='error', status='FAIL',
                             src='', detail='%s: %s' % (type(e).__name__, e)))
    return rows + problems, covered


def coverage(text, masked, covered, structural):
    """Every number token in the section must be either verified by a claim or explicitly
    classified as structural (index, formula constant, cross-reference, ...)."""
    struct_spans = []
    for rx, reason in structural:
        for m in re.finditer(rx, text):
            struct_spans.append((m.start(), m.end(), reason))
    out = []
    for kind, a, b, s in tokens(text, masked):
        cid = next((c for (x, y, c) in covered if x <= a and b <= y), None)
        if cid:
            out.append(dict(line=line_of(text, a), token=s, kind=kind, status='verified', by=cid)); continue
        before = text[max(0, a - 3):a]
        if kind == 'num' and re.search(r'[_^]\{?\(?$', before):
            out.append(dict(line=line_of(text, a), token=s, kind=kind, status='structural', by='index or exponent of a symbol')); continue
        reason = next((r for (x, y, r) in struct_spans if x <= a and b <= y), None)
        if reason:
            out.append(dict(line=line_of(text, a), token=s, kind=kind, status='structural', by=reason)); continue
        out.append(dict(line=line_of(text, a), token=s, kind=kind, status='UNACCOUNTED', by=''))
    return out


# ----------------------------------------------------------------------------- report
def write_report(path, rows, cov, repro, meta):
    esc = lambda v: str(v).replace('|', '\\|').replace('\n', ' ')
    rows = [{k: esc(v) if isinstance(v, str) else v for k, v in r.items()} for r in rows]
    cov = [{k: esc(v) if isinstance(v, str) else v for k, v in c.items()} for c in cov]
    with open(os.path.splitext(path)[0] + '.json', 'w') as f:
        json.dump(dict(meta=meta, checks=rows, tokens=cov, reproducibility=[{k: v for k, v in r.items() if k != 'ulp'} for r in repro]), f, indent=1, default=str)
    n = {k: sum(r['status'] == k for r in rows) for k in ('PASS', 'APPROX', 'FAIL')}
    un = [c for c in cov if c['status'] == 'UNACCOUNTED']
    L = ['# Verification of the numerical section', '']
    for k, v in meta.items():
        L.append('- **%s:** %s' % (k, v))
    L += ['', '## Summary', '',
          '| | count |', '|---|---|',
          '| checks passed (exact at printed precision, bitwise for inputs, or conclusion holds) | %d |' % n['PASS'],
          '| approximate statements within one unit of the last printed digit | %d |' % n['APPROX'],
          '| **checks failed** | **%d** |' % n['FAIL'],
          '| number tokens in the section | %d |' % len(cov),
          '| ... verified by a check | %d |' % sum(c['status'] == 'verified' for c in cov),
          '| ... structural (index, formula constant, label) | %d |' % sum(c['status'] == 'structural' for c in cov),
          '| **... not accounted for** | **%d** |' % len(un), '']
    if repro:
        L += ['## Reproducibility of the code output (stored results vs. re-executed now)', '',
              '| file | values compared | max ULP distance | bitwise identical |', '|---|---|---|---|']
        for r in repro:
            L.append('| %s | %d | %s | %s |' % (r['file'], r['n'], r['max_ulp'], 'yes' if r['identical'] else 'NO'))
        L.append('')
    fails = [r for r in rows if r['status'] == 'FAIL']
    if fails:
        L += ['## Failed checks', '', '| line | claim | printed | code output (rounded as printed) | full value | rule | detail |', '|---|---|---|---|---|---|---|']
        for r in fails:
            L.append('| %s | %s | %s | %s | %s | %s | %s |' % (r['line'], r['id'], r['printed'], r['computed'], r['full'], r['rule'], r['detail']))
        L.append('')
    if un:
        L += ['## Numbers not accounted for', '', '| line | token |', '|---|---|']
        for c in un:
            L.append('| %s | `%s` |' % (c['line'], c['token']))
        L.append('')
    L += ['## All checks', '', '| line | claim | printed | code output (rounded as printed) | full value | rule | status | source | detail |',
          '|---|---|---|---|---|---|---|---|---|']
    for r in sorted(rows, key=lambda r: (r['line'] if isinstance(r['line'], int) else 10 ** 9)):
        L.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (r['line'], r['id'], r['printed'], r['computed'], r['full'],
                                                                   r['rule'], r['status'], r.get('src', ''), r['detail']))
    L += ['', '## Every number token in the section', '', '| line | token | status | verified by / reason |', '|---|---|---|---|']
    for c in cov:
        L.append('| %s | `%s` | %s | %s |' % (c['line'], c['token'], c['status'], c['by']))
    open(path, 'w').write('\n'.join(L) + '\n')
    return n, un
