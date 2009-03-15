from __future__ import with_statement

import os
import unittest

def rel(path):
    return os.path.join(os.path.dirname(__file__), path)

class DiskTestCase(unittest.TestCase):
    def get_disk(self, filename):
        return rel(os.path.join('fixtures', filename))
