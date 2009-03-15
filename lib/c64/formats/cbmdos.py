"""This is a support module for all CBM-DOS formats."""
from __future__ import with_statement

import itertools
import struct

from c64 import struct_doc, blocks
from c64.bytestream import ByteStream

__all__ = [
    '_make_sector_table', 'FILE_TYPES',
    'DirectorySector', 'BootSector',
    'CircularFileError', 'FileNotFoundError', 'FormatError', 'IllegalSectorError'
    ]

class CircularFileError(Exception): pass
class FileNotFoundError(Exception): pass
class FormatError(Exception): pass
class IllegalSectorError(Exception): pass

FILE_TYPES = {
    0: "DEL",
    1: "SEQ",
    2: "PRG",
    3: "USR",
    4: "REL",
}

# C128 Boot Sector information:
#   http://www.atarimagazines.com/creative/v11n8/98_A_quick_quo_vadis_the_C1.php

# C128 address where the bootsector is loaded.
RAM_BOOTSECTOR = 0x0B00


class BootSector(object):
    """Represents a C128 boot sector.
    
    `load_address` is the address to load the referenced `filename`, if present.
    The bootsector itself is loaded into C128 memory at $0B00.
    """
    def __init__(self, bytes):
        self.load_address = 0
        self.bank = 0
        self.disk_block = 0
        self.diskname = ''
        self.filename = ''
        self.code_offset = 0
        self.code_address = 0
        self.code = ''

        self.is_valid = bytes.startswith('CBM')
        if self.is_valid:
            s = ByteStream(bytes[3:])
            self.load_address = s.word()
            self.bank = s.byte()
            self.disk_block = s.byte() # What?
            self.diskname = s.read_until(0, keep=False)
            self.filename = s.read_until(0, keep=False)
            self.code_offset = s.pos
            self.code_address = self.code_offset + RAM_BOOTSECTOR
            self.code = s.rest()


    @property
    def has_code(self):
        return self.code[0] != '\x00'
        
    def __str__(self):
        s = ["Valid bootloader: %s" % self.is_valid]
        if self.is_valid:
            s.append("Disk name: %s" % (self.diskname or "<None>"))
            s.append("File name: %s" % (self.filename or "<None>"))
            if self.filename:
                s.append("File load address: $%04x" % self.load_address)

            if self.has_code:
                s.append("Probable ML address: $%04x" % (self.code_address))
            
        return '\n'.join(s)


def _make_sector_table(sector_counts):
    l = list()
    for (start, end, sectors) in sector_counts:
        l.extend(itertools.repeat(sectors, end - start + 1))

    return l


class DirectoryEntry(object):
    """Represents a single CBM-DOS directory entry."""
    STRUCT_ENTRY = struct_doc('''
        <      # Little-endian
        xx     # Track/Sector of next Directory Sector (or 0 if not first entry in sector)
        B      # File Type
        BB     # Track/Sector of first File Sector
        16s    # Filename, PET-ASCII, $A0 padded
        xxx    # RELative file data
        xxxxxx # Unused (except with GEOS disks)
        H      # File size in sectors
        ''')

    
    def __init__(self, bytes):
        self.bytes = bytes
        
        self.typeflags, self.track, self.sector, self.raw_name, self.size =\
            struct.unpack(self.STRUCT_ENTRY, bytes)
            
        # Directory entries are padded to 16 characters with $A0.
        # Strip these off so we can print the names.
        self.name = self.raw_name.rstrip('\xa0')
        
    @property
    def filetype(self):
        return self.typeflags & 0x03
        
    @property
    def format(self):
        return FILE_TYPES[self.typeflags & 0x03]
        
    @property
    def splat(self):
        return self.typeflags & 0x80 == 0
        
    @property
    def locked(self):
        return self.typeflags & 0xC0
        
    def __str__(self):
        return "<Directory Entry '%s' %d (%d,%d)>" %\
            (self.name, self.size, self.track, self.sector)
    

class DirectorySector(object):
    """Represents a CBM-DOS directory sector (with multiple entries.)"""
    
    def __init__(self, bytes, track, sector):
        """Initialize this DirectorySector from a disk sector."""
        self.bytes = bytes
        self.location = (track, sector)
        self.next_sector = (bytes[0], bytes[1])
        self.entries = [DirectoryEntry(x) for x in blocks(bytes, 32)]
