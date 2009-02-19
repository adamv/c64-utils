"""Module for de-tokenizing C64 BASIC programs."""

from basic_tokens import *
from c64.formats import ByteStream

def map_quoted_char(c):
    return CONTROL_MAP.get(c, "{$%02x}" % (c))


class Basic(object):
    BASIC_RAM = 0x0801
    
    def __init__(self, bytes, has_header=True):
        """Initialize a Basic object from the given bytes."""
        self.bytes = ByteStream(bytes)
        
        self.load_address = self.BASIC_RAM
        # Skip the first two "program location" bytes if there is a header.
        # Might want to verify that they are $01,$80 -> $0801
        # ...or use this to switch off between C64/C128 token lists.
        if has_header:
            self.load_address = self.bytes.word()

    def list(self):
        prg = list()
        
        while not self.bytes.eof():
            link = self.bytes.word()
            if link == 0:
                break
                
            line = list()
            
            line.append(str(self.bytes.word()))
            line.append(' ')
            
            quote_mode = False
            
            # Parse this line...
            while True:
                c = self.bytes.byte()
                
                if c == 0:
                    # 0 ends the line
                    break
                elif c == 34:
                    # quote characters toggle quote_mode
                    quote_mode = not quote_mode
                    line.append(chr(c))
                elif not quote_mode and 0x80 <= c:
                    # Parse an opcode
                    opcode = TOKEN_MAP.get(c, "{UNKNOWN}")
                    line.append(opcode)
                else:
                    # ASCII or special quoted character
                    if 32 <= c <= 95:
                        line.append(chr(c))
                    else:
                        line.append(map_quoted_char(c))
                 
            prg.append(''.join(line))
        
        if not self.bytes.eof():
            ml_bytes = self.bytes.rest()
            prg.append("\n%d more bytes beyond end of BASIC program." % (len(ml_bytes)))
            
        return '\n'.join(prg)
