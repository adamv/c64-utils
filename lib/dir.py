#!/usr/bin/env python
from __future__ import with_statement

import sys
import os

from c64.formats import d64, d81, t64, basic
from c64.formats.cbmdos import GEOS_FILE_TYPES

_loaders = (
    ('.d64', d64.load),
    ('.t64', t64.load),
    ('.d81', d81.load),
    )
    

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
    """Get a loader that can handle a given image type."""

    for ext, loader in _loaders:
        if image_name.lower().endswith(ext):
            return loader

    raise Exception, "Unknown image type '%s'" % (image_name, )

def directory(image_name):
    loader = get_loader(image_name)
    d = loader(image_name)
    
    print
    print '%s: "%s", %2s' % (d.image_type, d.disk_name, d.disk_id)
    print
    
    print '###:  %-5s %-18s  Type' % ('Size','Name')
    print '----  %-5s %-18s  ----' % ('-'*4, '-'*18)
    for i, e in enumerate(d.entries):
        format = e.format
        if e.geos_type > 0:
            format += " (%s)" % (GEOS_FILE_TYPES.get(e.geos_type,'Unknown GEOS type: $%02x' % e.geos_type),)
    
        print '%3d:  %-5u %-18s  %s' % (
                i+1, e.size, '"'+e.name+'"', format)
        
    if d.has_bootsector:
        print
        print d.disk.bootsector

def extract_file(filename, bytes):
    outname = filename.strip() + '.prg'
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


def show_file(image_name, options, args):
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
            extract_file('sector-%d-%d' % (t,s), bytes)
        else:
            filename = args.pop(0)
            bytes = d.find(filename)
        
            if options.extract:
                extract_file(filename, bytes)
            else:
                show_basic(filename, bytes)
    except Exception, e:
        print e


USAGE = """
List the contents of a 1541 (d64) or 1581 (d81) disk image.

List the directory:
    ./dir.py <disk image name>
    
Display a file from the image, as detokenized BASIC:
    ./dir.py <disk image name> <file name>
    
Extract a file from the image:
    ./dir.py <disk image name> <file name> -e
    
Extract a single track/sector (such as a bootsector):
    ./dir.py <disk image name> -s1,0 -e
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
        show_file(image_name, options, args)
        return

    print USAGE

if __name__ == '__main__':
    main()
