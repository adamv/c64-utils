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

def directory(image_name):
    d = d64.load(image_name)
    print
    print 'Diskette "%s", %2s' % (d.disk_name, d.disk_id)
    print
    
    for e in d.entries:
        # Drop out when we get to empty entries
        # These should be filtered at a different level eventually
        if e.size == 0:
            break
        
        print "%-5u %-18s  %s" % (e.size, '"'+e.name+'"', e.format)

def show_file(image_name, filename):
    d = d64.load(image_name)
    
    try:
        dump_file(d.find(filename))
    except d64.FileNotFoundError, e:
        print e


USAGE = """
List the contents of a 1541 disk image (.D64)

List the directory:
    ./dir.py <disk image name>
    
Display a file from the image:
    ./dir.py <disk image name> <file name>
"""

if __name__ == '__main__':
    if len(sys.argv) == 2:
        directory(sys.argv[1])
    elif len(sys.argv) == 3:
        show_file(sys.argv[1], sys.argv[2])
    else:
        print USAGE
