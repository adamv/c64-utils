"Test PETSCII conversions."
from __future__ import with_statement

import sys
import os
import unittest

from c64.formats.petscii import *

class PetsciiTests(unittest.TestCase):
    def test_str(self):
        S1 = 'NORMAL'
        self.assertEqual(S1, petscii_str(S1))

    def test_chr(self):
        S1 = 'N'
        self.assertEqual(S1, quote_petscii(S1))

if __name__ == "__main__":
    unittest.main()
