"""This module provides support for reading "T64" tape images."""

from __future__ import with_statement
import struct
from c64 import struct_doc, blocks

class FileNotFoundError(Exception): pass
class FormatError(Exception): pass

TAPE_HEADER = struct_doc('''
<   # Little-endian
xx  # Tape version, unused
H   # Max no. of directory entries
xx  # Used directory entries; non-normative
xx  # Unused
24s # Tape name
''')

TAPE_ENTRY = struct_doc('''
<   # Little-endian
b   # C64s filetype
b   # CBM-DOS filetype
H   # Start address
H   # End address
xx  # Unused
L   # Byte-offset of start of file
xxxx # unused
16s # Filename, PET-ASCII, $20 padded
''')


class TapeEntry(object):
    def __init__(self, bytes):
        self.bytes = bytes
        
        self.c64s_filetype, self.filetype, self.start, self.end, self.offset, self.raw_name=\
            struct.unpack(TAPE_ENTRY, bytes)
            
        self.name = self.raw_name.strip()
            
    def __str__(self):
        return self.name
        
    def __repr__(self):
        return "<TapeEntry '%s'>" % (self.name)


class T64(object):
    def __init__(self, bytes):
        self.bytes = bytes
        self._validate()
        
        self.directory_size, self.raw_label =\
            struct.unpack(TAPE_HEADER, bytes[0x20:0x40])
            
        self.label = self.raw_label.strip()
        
        self.entries = [
            TapeEntry(x) for x in
            blocks(self.bytes, 0x20, offset=0x40, max=self.directory_size) ]
        
    def _validate(self):
        if not self.bytes.startswith('C64'):
            raise FormatError, "Invalid tape file."
            
    def __str__(self):
        return ", ".join(
            str(x) for x in 
            [self.directory_size, self.directory_entries, self.label] )

    def file(self, i):
        """Return file bytes for entry at index i."""
        e = self.entries[i]
        return self.bytes[e.start:e.end+1]
        
    def find(self, filename, ignore_case=False):
        for e in self.entries:
            if e.name == filename:
                return self.bytes[e.start:e.end+1]
        raise FileNotFoundError, 'File "%s" not found on tape.' % (filename)


def load(filename):
    with open(filename) as f:
        return T64(f.read())
