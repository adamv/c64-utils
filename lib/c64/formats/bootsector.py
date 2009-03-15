from c64.formats import format_bytes
from c64.bytestream import ByteStream

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
