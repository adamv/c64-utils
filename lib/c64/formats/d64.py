# Module - c64.formats.d64
# Provides support for reading "D64" disk images.

import struct

BYTES_PER_SECTOR = 256

def struct_doc(format):
    f = [x.partition('#')[0].strip() for x in format.splitlines()]
    return ''.join(f)


class IllegalSectorError(Exception): pass
class FormatError(Exception): pass
class CircularFileError(Exception): pass

entry_docs = """
    Disk type                  Size
    ---------                  ------
    35 track, no errors        174848
    35 track, 683 error bytes  175531
    40 track, no errors        196608
    40 track, 768 error bytes  197376

  Bytes: $00-1F: First directory entry
          00-01: Track/Sector location of next directory sector ($00 $00 if
                 not the first entry in the sector)
             02: File type.
                 Typical values for this location are:
                   $00 - Scratched (deleted file entry)
                    80 - DEL
                    81 - SEQ
                    82 - PRG
                    83 - USR
                    84 - REL
                 Bit 0-3: The actual filetype
                          000 (0) - DEL
                          001 (1) - SEQ
                          010 (2) - PRG
                          011 (3) - USR
                          100 (4) - REL
                          Values 5-15 are illegal, but if used will produce
                          very strange results. The 1541 is inconsistent in
                          how it treats these bits. Some routines use all 4
                          bits, others ignore bit 3,  resulting  in  values
                          from 0-7.
                 Bit   4: Not used
                 Bit   5: Used only during SAVE-@ replacement
                 Bit   6: Locked flag (Set produces ">" locked files)
                 Bit   7: Closed flag  (Not  set  produces  "*", or "splat"
                          files)
          03-04: Track/sector location of first sector of file
          05-14: 16 character filename (in PETASCII, padded with $A0)
          15-16: Track/Sector location of first side-sector block (REL file
                 only)
             17: REL file record length (REL file only, max. value 254)
          18-1D: Unused (except with GEOS disks)
          1E-1F: File size in sectors, low/high byte  order  ($1E+$1F*256).
                 The approx. filesize in bytes is <= #sectors * 254
"""

STRUCT_ENTRY = struct_doc('''
<   # Little-endian
xx  # Track/Sector of next Directory Sector (or 0 if not first entry in sector)
B   # File Type
BB  # Track/Sector of first File Sector
16s # Filename, PET-ASCII, $A0 padded
xxx # RELative file data
xxxxxx # Unused (except with GEOS disks)
H   # File size in sectors
''')


class DiskImage(object):
    """Represents the bytes of a D64 disk image used by C64 emulators.
    
    A D64 file represents the data bytes (and sometimes error codes) read
    off of a 5.25" 1541 disk. Usually these will be formatted using CBM-DOS,
    but not always (and sometimes the format is hand-crafted into a hybrid disk.)
    
    For flexibility, this class only handles the data bytes, accessible as sectors,
    and leaves CBM-DOS support for a higher-level class.
    
    But since it is a common trick, there is support for returning just the data
    bytes from a series of linked sectors.
    """

    sectors_per_track = (
        0, # Track numbering starts at 1
        21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21,
        19, 19, 19, 19, 19, 19, 19,
        18, 18, 18, 18, 18, 18,
        17, 17, 17, 17, 17,
        17, 17, 17, 17, 17, # For extended disks.
        )

    ## Sectors per track for each of 4 groups
    #sectors_per_group = (21, 19, 18, 17)
    ## The last numbered sector in each size group
    #last_sized_track = (17, 24, 30, 40)
    
    def __init__(self, bytes):
        self.bytes = bytes
        self._determine_tracks()

    def _determine_tracks(self):
        # Determine number of tracks
        if len(self.bytes) == 174848:
            self.tracks = 35
        elif len(self.bytes) == 196608:
            self.tracks = 40
        else:
            raise FormatError, "Cannot determine the number of tracks."
    
    def get_byte_offset(self, track, sector):
        "Returns the byte-offset of the given sector."
        ofs = sector + sum( 
            self.sectors_per_track[i] for i in range(1,track) )

        return ofs * BYTES_PER_SECTOR
    
    def get_sector(self, track, sector):
        ofs = self.get_byte_offset(track, sector)
        return self.bytes[ofs:ofs + BYTES_PER_SECTOR]
        
    def read_file(self, track, sector):
        """Read file bytes from the given starting track/sector, assuming the common
        "linked sectors" format used by CBM-DOS."""
        file_bytes = str()
        sectors_seen = set()

        while True:
            sectors_seen.add( (track, sector) )
            raw_bytes = self.get_sector(track, sector)
            track, sector = ord(raw_bytes[0]), ord(raw_bytes[1])
        
            good_bytes = 254
            # If there is no next track, then the "sector"
            # is actually the number of valid data bytes in 
            # this last sector.
            if track == 0:
                good_bytes = sector
        
            file_bytes += raw_bytes[2:2+good_bytes]
            
            if track == 0:
                break
                
            # If we've already seen the next sector in the chain
            # then this file has been hand-crafted to be a loop
            if (track, sector) in sectors_seen:
                raise CircularFileException, "Circular file detected"
        
        return file_bytes

    def __str__(self):
        return "<D64 Disk image: %d bytes, %d tracks>" % (len(self.bytes), self.tracks)

#STRUCT_ENTRY = '<xx B BB 16s xxx xxxxxx H'

class DirectoryEntry(object):
    """Represents a single CBM-DOS directory entry (8 per sector.)"""
    
    def __init__(self, bytes):
        self.bytes = bytes
        
        self.typeflags, self.track, self.sector, self.raw_name, self.size =\
            struct.unpack(STRUCT_ENTRY, bytes)
            
        # Directory entries are padded to 16 characters with $A0.
        # Strip these off so we can print the names.
        self.name = self.raw_name.rstrip('\xa0')
        
    def __str__(self):
        return "<Directory Entry '%s' %d (%d,%d)>" %\
            (self.name, self.size, self.track, self.sector)
    

class DirectorySector(object):
    """Represents a CBM-DOS directory sector (with multiple entries.)"""
    
    def __init__(self, bytes, track, sector):
        """Initialize this directory sector from a disk sector of 256 bytes."""
        self.bytes = bytes
        self.location = (track, sector)
        
        self.next_sector = (bytes[0], bytes[1])
        
        self.entries = list()
        for i in range(0, 8):
            ofs = i*32
            self.entries.append(DirectoryEntry(bytes[ofs:ofs+32]))

class DosDisk(object):
    """Represents a CBM-DOS formatted Disk Image."""
    # Number of bytes into the image for track 18 (directory)
    def __init__(self, disk):
        self.disk = disk
        self._read_directory()
        
    def _read_directory(self):
        # The Block Availability Map lives in track 18, sector 1
        self.BAM = self.disk.get_sector(18,0)
        
        self.directory_sectors = list()
        
        # Read the first directory listing sector
        # Initial track/sector of directory listing.
        t,s = 18,1
        while t != 0:
            # Get sector bytes
            sector_bytes = self.disk.get_sector(t, s)
            # Get the next track/sector
            t,s = ord(sector_bytes[0]), ord(sector_bytes[1])
            # Process these sector bytes
            self.directory_sectors.append(DirectorySector(sector_bytes, t, s))
    
    def entries(self):
        """Includes empty entries."""
        entries = list()
        for sector in self.directory_sectors:
            entries.extend(sector.entries)
        return entries
            
    def file(self, i):
        """Return file bytes for entry at index i."""
        e = list(self.entries())[i]
        return self.disk.read_file(e.track, e.sector)
    
    def __str__(self):
        return str(self.disk)
        #return "<D64 image: %d bytes, %d tracks>" % (len(self.bytes), self.tracks)

def load(filename):
    s = open(filename).read()
    return DosDisk(DiskImage(s))
