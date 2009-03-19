"""Module for de-tokenizing C64 BASIC programs."""

from basic_tokens import *
from c64.formats import *
import c64.bytestream

from c64.formats.petscii import quote_petscii

class BasicVersion(object):
    """Describes a BASIC version."""
    def __init__(self, start_address, format, tokens, description):
        self.start_address = start_address
        self.format = format
        self.tokens = tokens
        self.description = description
        
VERSIONS = (
    BasicVersion(0x0801, "Basic 2", TOKEN_MAP, "Basic 2 - C64"),
    BasicVersion(0, "Basic 7", None, "Basic 7 - C128"),
    )


class BasicLine(object):
    """Represents a single decoded line of BASIC."""

    def __init__(self, byte_count, line_number, line, unknown_opcode):
        self.byte_count = byte_count
        self.line_number = line_number
        self.line = line
        self.unknown_opcode = unknown_opcode

class Basic(object):
    """Represents a tokenized BASIC program."""
    
    BASIC_RAM = 0x0801
    
    def __init__(self, bytes, has_header=True, show_ml_bytes=True):
        """Initialize a Basic object from the given bytes."""
        self.bytes = c64.bytestream.ByteStream(bytes)
        self.show_ml_bytes = show_ml_bytes

        self.load_address = self.BASIC_RAM
        # Skip the first two "program location" bytes if there is a header.
        # Might want to verify that they are $01,$80 -> $0801
        # ...or use this to switch off between C64/C128 token lists.
        if has_header:
            self.load_address = self.bytes.word()
            
        self.listing = list()
        self.errors = list()
        self.parsed = False

    def verify(self):
        if not self.parsed:
            self.parse()
        
        line = -1
        for l in self.listing:
            if l.byte_count > 255:
                self.errors.append("Program line %d too long." % (l.line_number,))
                return False
            
            if l.line_number <= line:
                self.errors.append(
                    "Program lines are not in order (%d follows %s)." % (
                        l.line_number, line))
                return False

            line = l.line_number
            
        return True

    def list(self):
        if not self.parsed:
            self.parse()
            
        return self.report
        
    def parse(self):
        prg = list()
        
        while not self.bytes.eof():
            self.bytes.mark()
            
            link = self.bytes.word()
            if link == 0:
                break
            
            line_number = self.bytes.word()
            
            line = [str(line_number), ' ']
            quote_mode = False
            unknown_opcode = False

            # Parse this basic line; stop if we hit eof(), which means 
            # either the file is corrupt or it isn't a BASIC program.
            while not self.bytes.eof():
                c = self.bytes.byte()
                if c == 0:
                    break
                    
                if c == 34:
                    # quote characters toggle quote_mode
                    quote_mode = not quote_mode
                    line.append(chr(c))
                elif not quote_mode and 0x80 <= c:
                    # Parse an opcode token; they have the high bit set
                    opcode = TOKEN_MAP.get(c, "{UNKNOWN}")
                    unknown_opcode = unknown_opcode or opcode == '{UNKNOWN}'
                    line.append(opcode)
                else:
                    # Convert a "PETSCII" to host ASCII
                    line.append(quote_petscii(c))
                    
            text = ''.join(line)
            prg.append(text)

            self.listing.append(
                BasicLine(self.bytes.since_mark(), line_number, text, unknown_opcode))
        
        if not self.bytes.eof():
            self.ml_bytes = self.bytes.rest()
            n = len(self.ml_bytes)
            s = 's' if n != 1 else ''
            prg.append('\n%d more byte%s beyond end of BASIC program:' % (n, s))
            if self.show_ml_bytes:
                prg.append('%s' % format_bytes(self.ml_bytes))
            
        self.parsed = True
        self.report = '\n'.join(prg)
