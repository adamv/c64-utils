#!/usr/bin/env python
"A 6502 disassembler, designed for use with C64 programs."
from __future__ import with_statement
import sys
import os
import re
import itertools

import c64.bytestream
from c64.formats import basic, bootsector

from gdis.opcodes import *
from gdis.blocks import *


def parse_basic_header(options, r):
    if not options.basic_header:
        return ""

    b = basic.Basic(r.rest(), False)
    return b.list()


def read_symbols(filename):
    def rel(path):
        return os.path.join(os.path.dirname(__file__), path)

    def useful(lines):
        for x in lines:
            x = x.strip()
            if x and x[0] not in (';', '#'):
                yield x
    
    # Sample symbol file line:
    #   CINT    = $ff81 ; Initialize screen editor and video chip
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

def sym_to_int(d):
    """Convert an ASM hex to an integer."""
    return int(d.lstrip('$'),16)
    
def read_all_data(data):
    if not data:
        return list()

    # data_ranges will end up as a list of (start-address, len, comment) tuples
    # that define data blocks
    # Address is passed as a hex-string with no 0x, so covert to an int
    return [ (sym_to_int(x[0]), x[1], x[2]) for x in eval(data) ]
    
def read_all_comments(comments):
    if not comments:
        return list()
        
    return [Comment(sym_to_int(x[0]), x[1]) for x in eval(comments)]

def disassemble(options, args):
    symbols = read_all_symbols(options.symbol_files)
    data_ranges = read_all_data(options.data)
    comments_before = read_all_comments(options.comments)

    r = c64.bytestream.load(options.input_filename)

    if options.address:
        start_address = int(options.address, 16)
    elif options.bootsector:
        start_address = 0
    else:
        start_address = r.word()

    blocks = list()
    
    # Parse BASIC header, if requested
    basic_listing = parse_basic_header(options, r)
    
    boot = ""
    if options.bootsector:
        bs = bootsector.BootSector(r.rest())
        boot = str(bs)
        start_address = bs.code_address
        r = c64.bytestream.ByteStream(bs.code)

    # Now parse out ML
    address = start_address
    
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
        
    if boot:
        print "Boot Sector:"
        print boot
        print

    # Output!
    for b in blocks:
        print b

def main():
    from gdis.args import parse_args
    options, args = parse_args()
    disassemble(options, args)

if __name__ == "__main__":
    main()
