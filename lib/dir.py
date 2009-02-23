#!/usr/bin/env python

from __future__ import with_statement

import sys
from c64.formats import d64, t64, basic

def get_parser():
    from optparse import OptionParser

    p = OptionParser()
    opt = p.add_option

    # opt("-q", "--quiet", action="store_false", dest="verbose", default=True, 
    #     help="don't print status messages to stdout")
    #     
    # opt("-i", "--input", action="store", dest="input_filename")
    # opt("-a", "--addr", action="store", dest="address", default=None,
    #     help="Provide a load address, overriding one in the header if used.")
    # opt("-n", "--noheader", action="store_false", dest="use_header_address",
    #     help="Input file has no 2 byte load address header.")
    #     
    # opt("-s", "--symbols", dest="symbol_files", action="callback", callback=vararg_callback, default=())
        
    return p

def directory(image_name):
    d = d64.load(image_name)
    print
    print 'Diskette "%s", %2s' % (d.disk_name, d.disk_id)
    print
    
    for e in d.entries:
        print "%-5u %-18s  %s  (%d,%d)" % (e.size, '"'+e.name+'"', e.format, e.track, e.sector)
        
    print
    print d.disk.bootsector

def show_file(prg):
    print
    print "Load address:", prg.load_address
    if prg.load_address != prg.BASIC_RAM:
        print "(Non-standard load address, possible hybrid BASIC/ML program.)"
    print prg.list()

def extract_and_show(filename):
    if image_name.endswith('.d64'):
        loader = d64.load
    elif image_name.endswith('.t64'):
        loader = t64.load
    else:
        raise Exception, "Unknown image type '%s'" % (image_name, )
    
    d = loader(image_name)
    bytes = d.find(filename)
    print "Size:", len(bytes)
    prg = basic.Basic(bytes)
    show_file(prg)


USAGE = """
List the contents of a 1541 disk image (.D64)

List the directory:
    ./dir.py <disk image name>
    
Display a file from the image, as detokenized BASIC:
    ./dir.py <disk image name> <file name>
"""

if __name__ == '__main__':
    options, args = get_parser().parse_args()
    
    image_name = args.pop(0)
    
    if len(args) == 0:
        directory(image_name)
    elif len(args) == 1:
        filename = args.pop(0)
        try:
            extract_and_show(filename)
        except Exception, e:
            print e
    else:
        print USAGE
