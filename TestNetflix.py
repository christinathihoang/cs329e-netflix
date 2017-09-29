#!/usr/bin/env python3

# -------
# imports
# -------
from Netflix import netflix_eval
from unittest import main, TestCase
from math import sqrt
from io import StringIO
from numpy import sqrt, square, mean, subtract

# -----------
# TestNetflix
# -----------

class TestNetflix (TestCase):

    # ----
    # eval
    # ----

    def test_eval_1(self):
        r = StringIO("10:\n1952305\n1531863")
        w = StringIO()
        netflix_eval(r, w)
        self.assertEqual(
            w.getvalue(), "10\n3.3558579928839998\n3.252057992884\n0.30\n")

    def test_eval_2(self):
        r = StringIO("1000:\n2326571\n977808\n1010534\n1861759\n79755")
        w = StringIO()
        netflix_eval(r, w)
        self.assertEqual(
            w.getvalue(), "1000\n3.4684579928840003\n3.344457992884\n3.239857992884\n4.039857992884\n3.651457992884\n0.96\n")

    def test_eval_3(self):
        r = StringIO("10001:\n262828\n2609496\n1474804\n831991\n267142\n2305771\n220050")
        w = StringIO()
        netflix_eval(r, w)
        self.assertEqual(
            w.getvalue(), "10001\n3.5924579928840004\n3.9124579928839998\n3.7122579928839996\n3.279657992884\n3.885257992884\n3.550257992884\n3.572857992884\n0.66\n")

# ----
# main
# ----
if __name__ == '__main__':
    main()

""" #pragma: no cover
% coverage3 run --branch TestNetflix.py >  TestNetflix.out 2>&1



% coverage3 report -m                   >> TestNetflix.out



% cat TestNetflix.out
.
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
Name             Stmts   Miss Branch BrPart  Cover   Missing
------------------------------------------------------------
Netflix.py          27      0      4      0   100%
TestNetflix.py      13      0      0      0   100%
------------------------------------------------------------
TOTAL               40      0      4      0   100%

"""

