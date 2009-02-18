from __future__ import with_statement

import unittest
from c64.formats import format_bytes


class FormatsTests(unittest.TestCase):
    def test_a_few_bytes(self):
        s = format_bytes('\x00\x00\x01\x01')
        self.assertEqual(s, '00 00 01 01')

    def test_exact_row(self):
        s = format_bytes('\x00\x00\x01\x01', 2)
        self.assertEqual(s, '00 00\n01 01')

    def test_rows_and_extra(self):
        s = format_bytes('\x00\x00\x01\x01\x00', 2)
        self.assertEqual(s, '00 00\n01 01\n00')


if __name__ == "__main__":
    unittest.main()  
