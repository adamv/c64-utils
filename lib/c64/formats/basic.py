"""Module for de-tokenizing C64 BASIC programs."""

from basic_tokens import TOKEN_MAP
from c64.formats import ByteStream


class Basic(object):
    def __init__(self, bytes, has_header=True):
        """Initialize a Basic object from the given bytes."""
        self.bytes = ByteStream(bytes)
        
        self.load_address = 0x801
        # Skip the first two "program location" bytes if there is a header.
        # Might want to verify that they are $01,$80 -> $0801
        if has_header:
            self.load_addres = self.bytes.word()

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
                    #line.append( " {Toggled quote mode to %s} " % (quote_mode))
                    line.append(chr(c))
                elif c >= 0x80 and not quote_mode:
                    # Parse an opcode
                    opcode = TOKEN_MAP.get(c, "{UNKNOWN}")
                    line.append(opcode)
                else:
                    # ASCII or special quoted character
                    if 32 <= c <= 127:
                        line.append(chr(c))
                    else:
                        line.append("{%02x}" % (c))
                 
            prg.append(''.join(line))
        
        return '\n'.join(prg)
