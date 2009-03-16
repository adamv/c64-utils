"""This module provides support for reading "D64" (1541) disk images."""

from __future__ import with_statement

import struct

from c64 import struct_doc
from c64.formats.cbmdos import DosDisk, DiskImage, DiskDescription

class D64_Description(DiskDescription):
    """Describe the 1541 disk geometry and related CBM-DOS version."""
    
    _SECTOR_COUNTS = (
        # (starting track, ending track, sectors in this track group)
        (0, 0, 0),
        (1,  17, 21),
        (18, 24, 19),
        (25, 30, 18),
        (31, 35, 17))

#    sectors_per_track = _make_sector_table(_SECTOR_COUNTS)

    DIRECTORY_HEADER = (18, 0)
    DIRECTORY_ENTRIES = (18, 1)
    
    STRUCT_HEADER = struct_doc('''
<       # Little-endian
xx      # Track/sector of first directory block; should always be 18/1 for normal disks
x       # 'A' (representing "4040 format".)
x       # 0 ("Null flag for future DOS use.")
140x    # Block Allocation Map (BAM)
16s     # Disk name, PET-ASCII, $A0 padded
xx      # Two shift-spaces
2s      # Disk ID
x       # $A0
xx      # '2A' (DOS version and format type.)
xxxx    # Shifted spaces ($A0)
85x     # Rest of sector is unused.
''')


class D64Disk(DosDisk):
    def __init__(self, bytes):
        _desc = D64_Description()
        DosDisk.__init__(self, DiskImage(_desc, bytes),
                image_type="1541 Diskette")


def load(filename):
    with open(filename) as f:
        return D64Disk(f.read())
