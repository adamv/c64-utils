"""Support for bare files, aka 'prg' files."""

class PrgEntry(object):
    def __init__(self, name, bytes):
        self.bytes = bytes
        self.name = name
        self.raw_name = name

class PrgContainer(object):
    """Represents a container for PRG files.
    
    Bare files, such as .prg, don't have a "container" such as a D64 or T64.
    It is still useful to be able to treat bare files as their own container,
    to simplify logic for apps that work with various file types.
    """
    def __init__(self, name, bytes):
        self.bytes = bytes
        self.label = name
        self.raw_label = name
        self.entries = [PrgEntry(self.bytes, self.name)]

    def file(self, i):
        """Return file bytes for entry at index i."""
        return self.entries[i]
        
    def find(self, filename, ignore_case=False):
        if self.label == filename:
            return self.entries[0]

        raise FileNotFoundError, 'File "%s" not found on disk.' % (filename)
    
    def __str__(self):
        return '<PrgContainer "%s">' % (self.label,)
