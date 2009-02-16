#!/usr/bin/env python

from __future__ import with_statement

import sys
from c64.formats import d64

def dump_file(bytes):
    i = 0
    for x in bytes:
        sys.stdout.write("%02x " % ord(x))
        i += 1
        if i % 32 == 0:
            print
    print

d = d64.load("1984-05.d64")
print d

for f in d.entries():
    print f

#dump_file(d.file(1))
