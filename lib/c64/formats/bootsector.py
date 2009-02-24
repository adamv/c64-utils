from c64.formats import format_bytes

# C128 Boot Sector information:
#   http://www.atarimagazines.com/creative/v11n8/98_A_quick_quo_vadis_the_C1.php


class BootSector(object):
    """Represents a C128 boot sector."""
    def __init__(self, bytes):
        self.code = ''
        self.diskname = ''
        self.filename = ''
        self.load_address = 0
        self.bank = 0
        self.disk_block = 0
        self.is_valid = bytes.startswith('CBM')
        
        if self.is_valid:
            s = ByteStream(bytes[3:])
            self.load_address = s.word()
            self.bank = s.byte()
            self.disk_block = s.byte() # What?
            self.diskname = s.read_until(0, keep=False)
            self.filename = s.read_until(0, keep=False)
            self.code = s.rest()
        
    def __str__(self):
        s = ["Valid bootloader: %s" % self.is_valid]
        if self.is_valid:
            s.append("Disk name: %s" % (self.diskname or "<None>"))
            s.append("File name: %s" % (self.filename or "<None>"))
            s.append("Program bytes: (...)")
            #s.append("%s" % format_bytes(self.code))
            
        return '\n'.join(s)
