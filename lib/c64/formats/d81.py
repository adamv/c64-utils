"""This module provides support for reading "D81" (1581) disk images."""

from __future__ import with_statement

import struct

from c64 import struct_doc
from c64.formats.cbmdos import DosDisk, DiskImage, DiskDescription


"""
  Bytes:$00-01: Track/Sector location of the first directory sector (should
                be set to 40/3 but it doesn't matter, and don't trust  what
                is there, always go to 40/3 for first directory entry)
            02: Disk DOS version type (see note below)
                  $44 ('D')=1581
            03: $00
         04-13: 16 character Disk Name (padded with $A0)
         14-15: $A0
         16-17: Disk ID
            18: $A0
            19: DOS Version ("3")
            1A: Disk version ("D")
         1B-1C: $A0
         1D-FF: Unused (usually $00)
"""

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


class D81Disk(DosDisk):
    def __init__(self, bytes):
        _desc = D81_Description()
        DosDisk.__init__(self, DiskImage(_desc, bytes),
                image_type="1581 Diskette")


def load(filename):
    with open(filename) as f:
        return D81Disk(f.read())
