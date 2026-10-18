"""Parsing of numbers printed in LaTeX and the exact comparison rules.

A printed number is a *rounded* representation of a computed double. The comparison
"the printed value matches the code output exactly" is therefore made at the printed
precision: the exact binary value of the computed double, rounded half-up to the number of
decimals (fixed notation) or significant digits (a x 10^e notation) shown in the paper,
must be *identical* to the printed decimal. This is an exact test - no tolerance is
involved - and it is the strongest test a rounded number admits. Parameters that are
inputs of the code (e.g. r = 0.05) are compared with the configured double for bitwise
equality, float(printed) == configured.
"""
import re
from decimal import Decimal, ROUND_HALF_UP, getcontext
import math

getcontext().prec = 60

# a number as printed in LaTeX: 5\times10^{-13}, 2\times10^5, 10^{-14}, -0.2735, 15
NUM = r'(?:-?(?:\d+(?:\.\d+)?\\times\s*)?10\^\{?-?\d+\}?|-?\d+(?:\.\d+)?)'
NUM_RE = re.compile(r'(?<![A-Za-z0-9.\\])' + NUM)
WORDS = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8,
         'nine': 9, 'ten': 10, 'half': 0.5, 'halves': 0.5, 'twice': 2, 'second': 2, 'first': 1}
WORD_RE = re.compile(r'(?i)\b(' + '|'.join(WORDS) + r')\b')


class Printed:
    """A number as printed: value, and the precision at which it was rounded."""

    def __init__(self, s):
        self.s = s
        t = s.replace('\\times', 'x').replace(' ', '').replace('{', '').replace('}', '')
        m = re.fullmatch(r'(-?)(?:(\d+(?:\.\d+)?)x)?10\^(-?\d+)', t)
        if m:
            sign, mant, exp = m.group(1), m.group(2) or '1', int(m.group(3))
            self.kind = 'sci'
            self.mant = Decimal(sign + mant)
            self.exp = exp
            self.sig = len(mant.replace('.', '').lstrip('0')) or 1
            self.mant_dec = len(mant.split('.')[1]) if '.' in mant else 0
            self.value = self.mant * Decimal(10) ** exp
        else:
            self.kind = 'fixed'
            self.value = Decimal(t)
            self.dec = len(t.split('.')[1]) if '.' in t else 0
        self.float = float(self.value)

    def unit(self):
        """One unit in the last printed place."""
        if self.kind == 'fixed':
            return Decimal(1).scaleb(-self.dec)
        return Decimal(1).scaleb(self.exp - self.mant_dec)

    def round_like(self, x):
        """Round the exact binary value of x half-up to the printed precision."""
        d = Decimal(float(x))
        if self.kind == 'fixed':
            return d.quantize(Decimal(1).scaleb(-self.dec), rounding=ROUND_HALF_UP)
        m = (d / (Decimal(10) ** self.exp)).quantize(Decimal(1).scaleb(-self.mant_dec), rounding=ROUND_HALF_UP)
        return m * Decimal(10) ** self.exp

    def matches(self, x):
        return self.round_like(x) == self.value

    def fmt(self, x):
        r = self.round_like(x)
        if self.kind == 'fixed':
            return format(r, 'f')
        return '%se%d' % (format((r / Decimal(10) ** self.exp).normalize(), 'f'), self.exp)


def ulp_distance(a, b):
    """Distance between two doubles in units in the last place (0 = bitwise identical)."""
    a, b = float(a), float(b)
    if a == b:
        return 0.0
    if math.isnan(a) or math.isnan(b):
        return math.inf
    return abs(a - b) / math.ulp(max(abs(a), abs(b)))
