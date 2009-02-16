#!/usr/bin/env python

from __future__ import with_statement

import sys
from c64.formats import d64

d = d64.load("Master1.d64")
print d

for f in d.entries():
    print f

g = d.file(1)
i = 0
for x in g:
    sys.stdout.write("%02x " % ord(x))
    i += 1
    if i % 32 == 0:
        print
print
