"Unit tests for D64 images."
from __future__ import with_statement

import os
import unittest
from tests.disktest import DiskTestCase
from c64.formats import d64

class D64Tests(DiskTestCase):
    def test_load(self):
        d = d64.load(self.get_disk('1984-05.d64'))
        self.assertEquals("DISK SERVICE", d.disk_name)
        
    def test_entries(self):
        d = d64.load(self.get_disk('1984-05.d64'))
        self.assertEquals(50, len(d.entries))
        # raw_entries includes empty entries in the last directory sector
        self.assertEquals(56, len(d.raw_entries))
        
    def test_no_bootsector(self):
        d = d64.load(self.get_disk('1984-05.d64'))
        self.assertEqual(False, d.has_bootsector)
        
    def test_bootsector(self):
        d = d64.load(self.get_disk('BARD1A.d64'))
        self.assertEqual(True, d.has_bootsector, 
                "Expected to find a bootsector, but didn't.")

if __name__ == "__main__":
    unittest.main()  
