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

USAGE = """
List the contents of a 1541 disk image (.D64)

List the directory:
    ./dir.py <disk image name>
"""

if __name__ == '__main__':
    if len(sys.argv) == 2:
        d64.directory(sys.argv[1])
    else:
        print USAGE
