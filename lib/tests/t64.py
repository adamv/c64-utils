from __future__ import with_statement

import os
import unittest
from c64.formats import t64

def rel(path):
    return os.path.join(os.path.dirname(__file__), path)

class T64Tests(unittest.TestCase):
    def test_load(self):
        d = t64.load(rel("fixtures/paradrd.t64"))


if __name__ == "__main__":
    unittest.main()  
