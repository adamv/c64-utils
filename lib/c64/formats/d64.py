"""This module provides support for reading "D64" (1541) disk images."""

from __future__ import with_statement

import struct

from c64 import struct_doc, blocks
import c64.bytestream
from c64.formats import format_bytes
from c64.formats.cbmdos import *

STRUCT_HEADER = struct_doc('''
<       # Little-endian
xx      # Track/sector of first directory block; should always be 18/1 for normal disks
x       # 'A' (representing "4040 format".)
x       # 0 ("Null flag for future DOS use.")
140s    # Block Allocation Map (BAM)
16s     # Disk name, PET-ASCII, $A0 padded
xx      # Two shift-spaces
2s      # Disk ID
x       # $A0
xx      # '2A' (DOS version and format type.)
xxxx    # Shifted spaces ($A0)
85x     # Rest of sector is unused.
''')


class D64_Description(object):
    """Desribe the 1541 disk geometry and related CBM-DOS version."""
    BYTES_PER_SECTOR = 256
    
    sector_counts = (
        # (starting track, ending track, sectors in this track group)
        (0,  0,  0),
        (1,  17, 21),
        (18, 24, 19),
        (25, 30, 18),
        (31, 35, 17))

    DIRECTORY_HEADER = (18, 0)
    DIRECTORY_ENTRIES = (18, 1)
    
    def __init__(self):
        self.sectors_per_track = _make_sector_table(self.sector_counts)
        self.tracks = len(self.sectors_per_track) - 1


class DiskImage(object):
    """Handle standard Commodore Disk Images.
    
    This base class can handle retreiving individual or track/sector chains
    from a disk image, as described by `description`.
    
    This class has no specific knowledge of file or directory formats
    (other than being able to follow track/sector chains.)
    """

    def __init__(self, description, bytes):
        self._desc = description()
        self.bytes = bytes
        self.bootsector = BootSector(self.get_sector(1,0))

    @property
    def has_bootsector(self):
        return self.bootsector.is_valid

    def get_byte_offset(self, track, sector):
        "Return the byte-offset of the given sector."
        ofs = sector + sum(self._desc.sectors_per_track[i] for i in range(1,track))
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
        return "<Disk image: %d bytes, %d tracks>" % (
            len(self.bytes), self._desc.tracks)



class DosDisk(object):
    """Represents a CBM-DOS formatted 1541 Disk Image."""

    DIRECTORY_HEADER = (18, 0)
    DIRECTORY_ENTRIES = (18, 1)

    def __init__(self, 
            disk, 
            header_sector=None, entries_sector=None, 
            image_type='Abstract CBM DOS disk'):
        
        self.disk = disk
        self._read_directory()
        self.image_type = image_type
        
    def _read_directory(self):
        self.BAM, self.raw_disk_name, self.disk_id =\
            struct.unpack(
                STRUCT_HEADER,
                self.disk.get_sector( *self.DIRECTORY_HEADER ))

        self.disk_name = self.raw_disk_name.strip('\xA0')
        self.directory_sectors = [DirectorySector(*x)
            for x in self.disk.walk_sectors( *self.DIRECTORY_ENTRIES )]

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


def load(filename):
    with open(filename) as f:
        return DosDisk(DiskImage(D64_Description, f.read()))
