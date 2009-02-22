from __future__ import with_statement

import unittest
from c64 import blocks

# def blocks(bytes, block_size, offset=0, max=0):

class BlockTests(unittest.TestCase):
    def test_blocks(self):
        b = list (blocks('abcdefgh', 2))
        self.assertEquals(4, len(b))
        
    def test_max(self):
        b = list (blocks('abcdefgh', 2, max=2))
        self.assertEquals(2, len(b))
        
    def test_offset(self):
        b = list (blocks('abcdefgh', 2, offset=2))
        self.assertEquals(3, len(b))
        
if __name__ == "__main__":
    unittest.main()  
