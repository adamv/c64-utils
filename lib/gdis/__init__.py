#!/usr/bin/env python
from __future__ import with_statement
import sys
import os
import re
import itertools

from c64.formats import ByteStream
from gdis.opcodes import *
from gdis.blocks import *

def get_parser():
    from optparse import OptionParser

    def vararg_callback(option, opt_str, value, parser):
        assert value is None
        value = []

        def floatable(str):
            try:
                float(str)
                return True
            except ValueError:
                return False

        for arg in parser.rargs:
            # stop on --foo like options
            if arg[:2] == "--" and len(arg) > 2:
                break
            # stop on -a, but not on -3 or -3.0
            if arg[:1] == "-" and len(arg) > 1 and not floatable(arg):
                break
            value.append(arg)

        del parser.rargs[:len(value)]
        setattr(parser.values, option.dest, value)

    p = OptionParser()
    opt = p.add_option

    opt("-q", "--quiet", action="store_false", dest="verbose", default=True, 
        help="don't print status messages to stdout")
        
    opt("-i", "--input", action="store", dest="input_filename")
    opt("-a", "--addr", action="store", dest="address", default=None,
        help="Provide a load address, overriding one in the header if used.")
    opt("-n", "--noheader", action="store_false", dest="use_header_address",
        help="Input file has no 2 byte load address header.")
        
    opt("-s", "--symbols", dest="symbol_files", action="callback", callback=vararg_callback, default=())
        
    return p


def read_symbols(filename):
    def rel(path):
        return os.path.join(os.path.dirname(__file__), path)

    def useful(f):
        for x in f:
            x = x.strip()
            if x and x[0] not in (';', '#'):
                yield x
    
    # CINT    = $ff81 ; Initialize screen editor and video chip
    re_symbol = r"(\w+)\s*=\s*\$(\S+)(?:\s*;\s*(.*))?"
    symbols = list() # Will be a list of tuples (name, value, comment)
    
    if '.' not in filename:
        filename = rel('headers/'+filename+'.s')
        
    print "Reading symbols from",filename
    
    try:
        f = open(filename)
    except IOError:
        print 'Error reading file \"'+filename+'\"'
        return ()
        
    with f:
        for line in useful(f):
            m = re.match(re_symbol, line)
            if m:
                s = list(m.groups())
                s[1] = int(s[1], 16)
                symbols.append(s)

    return symbols


def main():
    options, args = get_parser().parse_args()

    symbols = list() # Will be a list of tuples (name, value, comment)
    for f in options.symbol_files:
        symbols.extend(read_symbols(f))

    data_ranges = ()
    comments_before = ()
    comments_before = sorted(comments_before, key=lambda x: x.address.addr)

    with open(options.input_filename, 'rb') as f:
        r = ByteStream(f.read())

    if options.address is None: # if has_start_adress_header:
        start_address = r.word()
    else:
        start_address = int(options.address, 16)

    address = start_address
    blocks = list()
    while not r.eof():
        found_data_block = False
        
        # if in data range...
        for x in data_ranges:
            if x[0] == address:
                data = r.chars(x[1]-x[0]+1)
                blocks.append(AsciiData(address, data))
                address = x[1]+1
                found_data_block = True
                break
    
        if found_data_block:
            continue
    
        # Decode operation
        o = r.byte()
        op = op_map.get(o, None)
        if op is None:
            blocks.append(DataByte(address, o))
            address += 1
            continue

        operand = None
        try:
            operand = op.read_operand(r)
        except IndexError: pass
        
        blocks.append(Instruction(address, op, operand))
        address += op.bytes

    # Assign labels to operands
    for b in blocks:
        b.pull_labels(symbols)

    # Merge comments
    blocks = sorted(itertools.chain(comments_before, blocks), key=lambda x: x.address.addr)

    print "Load address: $%04X" % (start_address)
    print

    # Output!
    for b in blocks:
        print b

if __name__ == "__main__":
    main()
