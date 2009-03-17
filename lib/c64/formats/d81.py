"""This module provides support for reading "D81" (1581) disk images."""

from __future__ import with_statement

import struct

from c64 import struct_doc
from c64.formats.cbmdos import DosDisk, DiskImage, DiskDescription


class D81_Description(DiskDescription):
    """Describe the 1541 disk geometry and related CBM-DOS version."""
    
    _SECTOR_COUNTS = (
        # (starting track, ending track, sectors in this track group)
        (0, 0, 0),
        (1, 80, 40))

    DIRECTORY_HEADER = (40, 0)
    DIRECTORY_ENTRIES = (40, 3)
    
    STRUCT_HEADER = struct_doc('''
<       # Little-endian
xx      # Track/sector of first directory block; 40/3 for normal disks
x       # 'D' (representing "4040 format".)
x       # 0 Null byte.
16s     # Disk name, PET-ASCII, $A0 padded
xx      # Two shift-spaces
2s      # Disk ID
x       # $A0
xx      # '3D' (DOS version and format type.)
xx      # Shifted spaces ($A0)
227x    # Rest of sector is unused.
''')


_desc = D81_Description()

class D81Disk(DosDisk):
    def __init__(self, bytes):
        DosDisk.__init__(self, DiskImage(_desc, bytes),
                image_type="1581 Diskette")


def load(filename):
    with open(filename) as f:
        return D81Disk(f.read())
