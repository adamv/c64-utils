# Module - c64.formats.d64
# Provides support for reading "D64" disk images.

from __future__ import with_statement
import struct

BYTES_PER_SECTOR = 256

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

def blocks(bytes, block_size):
    i = 0
    while i < len(bytes):
        yield bytes[i:i+block_size]
        i += block_size


def struct_doc(format):
    'A silly function to allow "readable" struct formats.'
    return ''.join(
        x.partition('#')[0].strip() for x in format.splitlines() )


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


class DiskImage(object):
    """Represents the bytes of a D64 disk image used by C64 emulators.
    
    This class can retreive sector data, but has no knowledge of file or directory formats
    except for being able to walk a chain of linked sectors.
    """

    sectors_per_track = (
        0, # Track numbering starts at 1
        21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21,
        19, 19, 19, 19, 19, 19, 19,
        18, 18, 18, 18, 18, 18,
        17, 17, 17, 17, 17,
        17, 17, 17, 17, 17, # For extended disks.
        )

    def __init__(self, bytes):
        self.bytes = bytes
        self._determine_tracks()

    def _determine_tracks(self):
        if len(self.bytes) == 174848:
            self.tracks = 35
        elif len(self.bytes) == 196608:
            self.tracks = 40
        else:
            raise FormatError, "Cannot determine the number of tracks."
    
    def get_byte_offset(self, track, sector):
        "Return the byte-offset of the given sector."
        ofs = sector + sum(self.sectors_per_track[i] for i in range(1,track))
        return ofs * BYTES_PER_SECTOR
    
    def get_sector(self, track, sector):
        ofs = self.get_byte_offset(track, sector)
        return self.bytes[ofs:ofs + BYTES_PER_SECTOR]
        
    def walk_sectors(self, track, sector, callback):
        """Walks a chain of linked sectors, using the given callback."""
        sectors_seen = set()

        while track > 0:
            if (track, sector) in sectors_seen:
                raise CircularFileError, "Circular file detected: %s, %s" % ((track, sector), sectors_seen)

            sectors_seen.add( (track, sector) )
            raw_bytes = self.get_sector(track, sector)
            track, sector = ord(raw_bytes[0]), ord(raw_bytes[1])
            
            callback(raw_bytes, track, sector)
            
    def read_file(self, track, sector):
        """Read file bytes from the given starting track/sector, assuming 
        the common "linked sectors" format used by CBM-DOS."""
        file_bytes = [str()]

        def cb(block, next_track, next_sector):
            # If there is no next track, then the "sector"
            # is actually the number of valid data bytes
            data_count = 254 if next_track > 0 else next_sector
            file_bytes[0] += block[2:2+data_count]
            
        self.walk_sectors(track, sector, cb)
        return file_bytes[0]

    def __str__(self):
        return "<D64 Disk image: %d bytes, %d tracks>" % (len(self.bytes), self.tracks)


class DirectoryEntry(object):
    """Represents a single CBM-DOS directory entry."""
    
    def __init__(self, bytes):
        self.bytes = bytes
        
        self.typeflags, self.track, self.sector, self.raw_name, self.size =\
            struct.unpack(STRUCT_ENTRY, bytes)
            
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


class DosDisk(object):
    """Represents a CBM-DOS formatted Disk Image."""
    
    def __init__(self, disk):
        self.disk = disk
        self._read_directory()
        
    def _read_directory(self):
        self.BAM, self.raw_disk_name, self.disk_id =\
            struct.unpack(STRUCT_HEADER, self.disk.get_sector(18,0))
            
        self.disk_name = self.raw_disk_name.strip('\xA0')
        self.directory_sectors = list()

        def cb(block, t, s):
            self.directory_sectors.append(DirectorySector(block, t, s))

        self.disk.walk_sectors(18, 1, cb)
    
    @property
    def entries(self):
        """Includes empty entries."""
        entries = list()
        for sector in self.directory_sectors:
            entries.extend(sector.entries)
        return entries
            
    def file(self, i):
        """Return file bytes for entry at index i."""
        e = list(self.entries)[i]
        return self.disk.read_file(e.track, e.sector)
        
    def find(self, filename):
        for e in self.entries:
            if e.name == filename:
                return self.disk.read_file(e.track, e.sector)
        raise FileNotFoundError, 'File "%s" not found on disk.' % (filename)
    
    def __str__(self):
        return '<DosDisk "%s" "%s">' % (self.disk_name, self.disk_id)


def load(filename):
    s = open(filename).read()
    return DosDisk(DiskImage(s))
