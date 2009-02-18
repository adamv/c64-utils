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
        "Read the next two bytes from the stream, and convert them to an integer (little-endian)."
        lo = ord(self.bytes[self._i])
        hi = ord(self.bytes[self._i+1])
        self._i += 2
        return lo + hi*256
        
    def byte(self):
        "Read the next byte form the strea, and convert to an integer."
        lo = ord(self.bytes[self._i])
        self._i += 1
        return lo
        
    def rest(self):
        "Return the unread bytes from this stream."
        return self.bytes[self._i:]
        
    def dump(self):
        "Return a hex representation of the bytes remaining in this stream."
        return ' '.join(['%02X' % (ord(b)) for b in r.rest()])

    def eof(self):
        "Are we at the end of the stream?"
        return self._i >= len(self.bytes)

    def read_until(self, b, keep=True):
        "Return a string up to the character or byte 'b', or the end of the string if b isn't found."
        # b can be a character or integer
        if isinstance(b, int):
            b = chr(b)
        
        j = self._i
        while j < len(self.bytes) and self.bytes[j] != b:
            j += 1
        
        cut_off = j+1 if keep else j
        result = self.bytes[self._i:cut_off]

        self._i = j+1

        return result
