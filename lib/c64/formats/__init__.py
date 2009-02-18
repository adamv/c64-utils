def format_bytes(bytes, bytes_per_line=32):
    rows = list()
    
    row = list()
    for i, x in enumerate(bytes):
        row.append("%02x" % ord(x))

        if (i+1) % bytes_per_line == 0:
            rows.append(' '.join(row))
            row = list()
    
    if row:
        rows.append(' '.join(row))
        
    return '\n'.join(rows)


class ByteStream(object):
    """Represents a stream of little-endian bytes (stored originally as a string)."""
    
    def __init__(self, s):
        self.bytes = s
        self._i = 0
        
    def word(self):
        lo = ord(self.bytes[self._i])
        hi = ord(self.bytes[self._i+1])
        self._i += 2
        return lo + hi*256
        
    def byte(self):
        lo = ord(self.bytes[self._i])
        self._i += 1
        return lo
        
    def rest(self):
        return self.bytes[self._i:]
        
    def dump(self):
        return ' '.join(['%02X' % (ord(b)) for b in r.rest()])

    def eof(self):
        return self._i >= len(self.bytes)

    def read_until(self, b, keep=True):
        # b can be a character or integer
        if isinstance(b, int):
            b = chr(b)
        
        j = self._i
        while j < len(self.bytes) and self.bytes[j] != b:
            j += 1
            
        if keep:
            result = self.bytes[self._i:j+1]
        else:
            result = self.bytes[self._i:j]
            
        self._i = j+1

        return result
