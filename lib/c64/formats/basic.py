"""Module for de-tokenizing C64 BASIC programs."""

from basic_tokens import TOKEN_MAP

class ByteStream(object):
    """Represents a stream of little-endian bytes (stored originally as a string)."""
    
    def __init__(self, s):
        self.bytes = list(ord(c) for c in s)
        
    def word(self):
        lo = self.bytes.pop(0)
        hi = self.bytes.pop(0)
        return lo + hi*256
        
    def byte(self):
        return self.bytes.pop(0)
        
    def rest(self):
        return self.bytes[:]
        
    def dump(self):
        return ' '.join(['%02X' % (b) for b in r.rest()])

    def eof(self):
        return not len(self.bytes)


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
