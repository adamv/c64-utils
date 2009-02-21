"Unit tests for D64 images."
from __future__ import with_statement

import os
import unittest
from c64.formats import d64

def rel(path):
    return os.path.join(os.path.dirname(__file__), path)

class D64Tests(unittest.TestCase):
    def test_load(self):
        d = d64.load(rel('fixtures/1984-05.d64'))
        self.assertEquals("DISK SERVICE", d.disk_name)

if __name__ == "__main__":
    unittest.main()  
