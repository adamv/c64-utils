"""This module provides support for reading "D81" (1581) disk images."""

from __future__ import with_statement

from cbmdos import *

def load(filename):
    with open(filename) as f:
        return DosDisk(DiskImage(D81_Description, f.read()))
