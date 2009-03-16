"Unit tests for D81 images."
from __future__ import with_statement

import os
import unittest
from tests.disktest import DiskTestCase
from c64.formats import d81


class D81Tests(DiskTestCase):
    def test_load(self):
        d = d81.load(self.get_disk('bbs/drive8.d81'))
        self.assertEquals("bbs1", d.disk_name)
        
    def test_entries(self):
        d = d81.load(self.get_disk('bbs/drive8.d81'))
        self.assertEquals(145, len(d.entries))


if __name__ == "__main__":
    unittest.main()  
