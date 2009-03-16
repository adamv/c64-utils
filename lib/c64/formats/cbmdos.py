"""This is a support module for all CBM-DOS formats."""
from __future__ import with_statement

import itertools
import struct

from c64 import struct_doc, blocks
from c64.bytestream import ByteStream

__all__ = [
    'FILE_TYPES',
    'DirectorySector', 'BootSector',
    'DiskImage', 'DosDisk', 'DiskDescription',
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


class DiskDescription(object):
    BYTES_PER_SECTOR = 256

    def __init__(self):
        self.sectors_per_track = _make_sector_table(self._SECTOR_COUNTS)


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


class DiskImage(object):
    """Handle standard Commodore Disk Images.
    
    This base class can handle retreiving individual or track/sector chains
    from a disk image, as described by `description`.
    
    This class has no specific knowledge of file or directory formats
    (other than being able to follow track/sector chains.)
    """

    def __init__(self, description, bytes):
        self._desc = description
        self.bytes = bytes
        self.bootsector = BootSector(self.bytes[0:256])

    @property
    def has_bootsector(self):
        return self.bootsector.is_valid

    def get_byte_offset(self, track, sector):
        "Return the byte-offset of the given sector."
        ofs = sector + sum(self._desc.sectors_per_track[i] for i in range(1, track))
        return ofs * self._desc.BYTES_PER_SECTOR
    
    def get_sector(self, track, sector):
        ofs = self.get_byte_offset(track, sector)
        return self.bytes[ofs:ofs + self._desc.BYTES_PER_SECTOR]
        
    def walk_sectors(self, track, sector):
        sectors_seen = set()

        while track > 0:
            if (track, sector) in sectors_seen:
                raise CircularFileError, "Circular file detected: %s, %s" % (
                    (track, sector), sectors_seen)

            sectors_seen.add( (track, sector) )
            raw_bytes = self.get_sector(track, sector)
            track, sector = ord(raw_bytes[0]), ord(raw_bytes[1])
            yield raw_bytes, track, sector
            
    def read_file(self, track, sector):
        """Read file bytes from the given starting track/sector, assuming 
        the common "linked sectors" format used by CBM-DOS."""
        
        file_bytes = list()
        
        for (block, t, s) in self.walk_sectors(track, sector):
            byte_size = 254 if t > 0 else s
            file_bytes.append(block[2:2+byte_size])

        return ''.join(file_bytes)

    def __str__(self):
        return "<Disk image: %d bytes>" % (len(self.bytes))


class DosDisk(object):
    """Represents a CBM-DOS formatted Disk Image."""

    def __init__(self, 
            disk, 
            header_sector=None, entries_sector=None, 
            image_type='Abstract CBM DOS disk'):
        
        self.disk = disk
        self._desc = disk._desc
        self._read_directory()
        self.image_type = image_type
        
    def _read_directory(self):
        self.BAM, self.raw_disk_name, self.disk_id =\
            struct.unpack(
                self._desc.STRUCT_HEADER,
                self.disk.get_sector( *self._desc.DIRECTORY_HEADER ))

        self.disk_name = self.raw_disk_name.strip('\xA0')
        self.directory_sectors = [DirectorySector(*x)
            for x in self.disk.walk_sectors( *self._desc.DIRECTORY_ENTRIES )]

        self.raw_entries = [e for s in self.directory_sectors for e in s.entries]
        self.entries = [e for e in self.raw_entries if e.size > 0]
            
    def file(self, i):
        """Return file bytes for entry at index i."""
        e = self.entries[i]
        return self.disk.read_file(e.track, e.sector)
        
    def find(self, filename, ignore_case=False):
        for e in self.entries:
            if e.name == filename:
                return self.disk.read_file(e.track, e.sector)
        raise FileNotFoundError, 'File "%s" not found on disk.' % (filename)
    
    def __str__(self):
        return '<DosDisk: %s "%s" "%s">' % (
            self.image_type, self.disk_name, self.disk_id)
        
    @property
    def has_bootsector(self):
        return self.disk.has_bootsector
