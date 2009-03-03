#!/usr/bin/env python
from __future__ import with_statement

import sys
import os

from c64.formats import d64, t64, basic

def parse_args():
    from optparse import OptionParser

    p = OptionParser()
    op = p.add_option
    
    op('-e', '--extract', 
        action='store_true',
        help='Extract and save file instead of listing.')

    op('-s', '--sector',
        dest='sector',
        help='Track,sector to extract from a disk image.')
        
    return p.parse_args()

def get_loader(image_name):
    """Get a loader class that can handle a given image."""
    if image_name.endswith('.d64'):
        return d64.load
    
    if image_name.endswith('.t64'):
        return t64.load

    raise Exception, "Unknown image type '%s'" % (image_name, )

def directory(image_name):
    d = d64.load(image_name)
    
    print
    print 'Diskette "%s", %2s' % (d.disk_name, d.disk_id)
    print
    
    for e in d.entries:
        print '%-5u %-18s  %s  (%d,%d)' % (e.size, '"'+e.name+'"', e.format, e.track, e.sector)
        
    print
    print d.disk.bootsector

def extract_file(filename, bytes):
    outname = filename+'.prg'
    if os.path.exists(outname):
        print "File '%s' already exists, aborting for safety." % (outname,)
        return

    with open(outname, 'wb') as f:
        f.write(bytes)

    print "Wrote %d bytes to %s." % (len(bytes), outname)
        
def show_basic(filename, bytes):
    prg = basic.Basic(bytes)

    print
    print "Load address:", prg.load_address
    if prg.load_address != prg.BASIC_RAM:
        print "(Non-standard load address, possible hybrid BASIC/ML program.)"

    print prg.list()


USAGE = """
List the contents of a 1541 disk image (.D64)

List the directory:
    ./dir.py <disk image name>
    
Display a file from the image, as detokenized BASIC:
    ./dir.py <disk image name> <file name>
"""

def main():
    options, args = parse_args()
    image_name = args.pop(0)
    
    show_dir = (len(args) == 0) and (not options.sector)
    if show_dir:
        directory(image_name)
        return
        
    show_listing = (len(args) == 1) or (options.sector)
    if show_listing:
        try:
            loader = get_loader(image_name)
            d = loader(image_name)
            
            if options.sector:
                if not options.extract:
                    print USAGE
                    return

                t,s = options.sector.split(',')
                t = int(t)
                s = int(s)
                
                bytes = d.disk.get_sector(t,s)
                extract_file('bootsector', bytes)
            else:
                filename = args.pop(0)
                bytes = d.find(filename)
            
                if options.extract:
                    extract_file(filename, bytes)
                else:
                    show_basic(filename, bytes)
        except Exception, e:
            print e
            
        return

    print USAGE

if __name__ == '__main__':
    main()
