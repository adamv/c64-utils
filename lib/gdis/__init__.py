#!/usr/bin/env python
"A 6502 disassembler, designed for use with C64 programs."
from __future__ import with_statement
import sys
import os
import re
import itertools

import c64.bytestream
import c64.formats.basic

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
    op = p.add_option

    op('-i', '--input', action='store', dest='input_filename')
    op('-a', '--addr', action='store', dest='address', default=None,
        help='Provide a load address, overriding one in the header if used.')
        
    op('-n', '--noheader', action='store_false', dest='use_header_address',
        help='Input file has no 2 byte load address header.')
        
    op('-b', '--basic', action='store_true', dest='basic_header',
        help='Try to parse a BASIC program header before ML.')
        
    op('-o', '--offset', type='int', dest='offset', default=0,
        help='Offset at which to start disassembly.')
        
    op('-d', '--data', default=None,
        help='A Python list of tuples that defines data blocks; will be moved to a config file format.')
        
    op('-c', '--comments', default=None,
        help='A Python list of ("address", "comment") tuples; will be moved to a config file format.')
    
    op('-s', '--symbols', dest='symbol_files', action='callback', callback=vararg_callback, default=())
        
    return p

def parse_args():
    return get_parser().parse_args()    

def parse_basic_header(options, r):
    if not options.basic_header:
        return ""

    b = c64.formats.basic.Basic(r.rest(), False)
    return b.list()


def read_symbols(filename):
    def rel(path):
        return os.path.join(os.path.dirname(__file__), path)

    def useful(lines):
        for x in lines:
            x = x.strip()
            if x and x[0] not in (';', '#'):
                yield x
    
    # CINT    = $ff81 ; Initialize screen editor and video chip
    re_symbol = r"(\w+)\s*=\s*\$(\S+)(?:\s*;\s*(.*))?"
    
    # Symbol files with no extension are read from built-ins in "headers"
    if '.' not in filename:
        filename = rel('headers/'+filename+'.s')
        
    try:
        with open(filename) as f:
            lines = f.readlines()
    except IOError:
        print 'Error reading file \"'+filename+'\"'
        return ()
        
    symbols = list() # Will be a list of tuples (name, value, comment)
    for x in useful(lines):
        m = re.match(re_symbol, x)
        if m:
            s = list(m.groups())
            s[1] = int(s[1], 16)
            symbols.append(s)

    return symbols
    
def read_all_symbols(filenames):
    "Return a list of tuples (name, value, comment) read from given symbol filenames."
    s = list() 
    for f in filenames:
        s.extend(read_symbols(f))

    return s
    
def read_all_data(data):
    if not data:
        return list()

    # data_ranges will end up as a list of (start-address, len, comment) tuples
    # that define data blocks
    # Address is passed as a hex-string with no 0x, so covert to an int
    return [ (int(x[0].lstrip('$'),16), x[1], x[2]) for x in eval(data) ]
    
def read_all_comments(comments):
    if not comments:
        return list()
        
    return [Comment(int(x[0].lstrip('$'),16), x[1]) for x in eval(comments)]

def disassemble(options, args):
    symbols = read_all_symbols(options.symbol_files)
    data_ranges = read_all_data(options.data)
    comments_before = read_all_comments(options.comments)

    r = c64.bytestream.load(options.input_filename)

    if options.address is None: # if has_start_adress_header:
        start_address = r.word()
    else:
        start_address = int(options.address, 16)

    address = start_address
    blocks = list()
    
    # Parse BASIC header, if requested
    basic_listing = parse_basic_header(options, r)

    # Now parse out ML
    
    # Jump to the offset if specified
    if options.offset:
        r.reset(options.offset)
        address += options.offset-2 # Jump back 2 bytes for load header; FIXME

    while not r.eof():
        # print address, r.pos, data_ranges[0]
        found_data_block = False
        
        # if in a data range...
        for x in data_ranges:
            if x[0] == address:
                data = r.chars(x[1])
                blocks.append(AsciiData(address, data))
                comments_before.append(Comment(address, x[2]))
                
                address += x[1]
                
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
    comments_before = sorted(comments_before, key=lambda x: x.address.addr)
    blocks = sorted(itertools.chain(comments_before, blocks), key=lambda x: x.address.addr)

    print "Load address: $%04X" % (start_address)
    print
    if basic_listing:
        print "BASIC header:"
        print basic_listing
        print

    # Output!
    for b in blocks:
        print b

def main():
    options, args = parse_args()
    disassemble(options, args)

if __name__ == "__main__":
    main()
