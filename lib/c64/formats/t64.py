import struct

def struct_doc(format):
    #f = [x.partition('#')[0].strip() for x in format.splitlines()]
    return ''.join(x.partition('#')[0].strip() for x in format.splitlines())

class FormatError(Exception): pass

tape_header_docs = """
Bytes:$20-21: Tape version number of either $0100 or $0101. I am  not  sure
              what differences exist between versions.
       22-23: Maximum  number  of  entries  in  the  directory,  stored  in
              low/high byte order (in this case $0190 = 400 total)
       24-25: Total number of used entries, once again  in  low/high  byte.
              Used = $0005 = 5 entries.
       26-27: Not used
       28-3F: Tape container name, 24 characters, padded with $20 (space)
"""

TAPE_HEADER = struct_doc('''
<   # Little-endian
xx  # Tape version, unused
H   # Max no. of directory entries
H   # Used directory entries; non-normative
xx  # Unused
24s # Tape name
''')

tape_entry_docs = """
Bytes   $40: C64s filetype
                  0 = free (usually)
                  1 = Normal tape file
                  3 = Memory Snapshot, v .9, uncompressed
              2-255 = Reserved (for memory snapshots)
         41: 1541 file type (0x82 for PRG, 0x81 for  SEQ,  etc).  You  will
             find it can vary  between  0x01,  0x44,  and  the  normal  D64
             values. In reality any value that is not a $00 is  seen  as  a
             PRG file. When this value is a $00 (and the previous  byte  at
             $40 is >1), then the file is a special T64 "FRZ" (frozen) C64s
             session snapshot.
      42-43: Start address (or Load address). This is the first  two  bytes
             of the C64 file which is usually the load  address  (typically
             $01 $08). If the file is a snapshot, the address will be 0.
      44-45: End address (actual end address in memory,  if  the  file  was
             loaded into a C64). If  the  file  is  a  snapshot,  then  the
             address will be a 0.
      46-47: Not used
      48-4B: Offset into the conatiner file (from the beginning)  of  where
             the C64 file starts (stored as low/high byte)
      4C-4F: Not used
      50-5F: C64 filename (in PETASCII, padded with $20, not $A0)
"""

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
        
        self.c64s_filetype, self.filetype, self.start, self.end, self.offset, self.name=\
            struct.unpack(TAPE_ENTRY, bytes)
            
    def __str__(self):
        return self.name
        
    def __repr__(self):
        return "<TapeEntry '%s'>" % (self.name)


class T64(object):
    def __init__(self, bytes):
        self.bytes = bytes
        self._read_directory()
        self.validate()
        
        self.directory_size, self.directory_entries, self.raw_label =\
            struct.unpack(TAPE_HEADER, bytes[0x20:0x40])
            
        self.label = self.raw_label.trim()
            
        self.contents = list()
        for i in range(0, self.directory_size):
            ofs = 0x40 + i * 0x20
            self.contents.append(TapeEntry(self.bytes[ofs:ofs+0x20]))
        
#        self.typeflags, self.track, self.sector, self.raw_name, self.size =\
#            struct.unpack(STRUCT_ENTRY, bytes)

        
    def _read_directory(self):
        pass
        
    def validate(self):
        if not self.bytes.startswith('C64'):
            raise FormatError, "Invalid tape file."
            
    def __str__(self):
        return ", ".join(str(x) for x in [self.directory_size, self.directory_entries, self.label])


def load(filename):
    s = open(filename).read()
    return T64(s)
