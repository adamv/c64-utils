"""This module defines the abstract 'file container' interfaces."""

class FileContaner(object):
    """Represents a container for files or program data.
    
    A container has a name and a list of entries, at a minimum, as well
    as format-specific methods and properties.
    """
    
    @property
    def entries(self):
        """A list of entries in this container.
        
        Some containers may have "empty" entries. For instance,
        a D64 directory sector may only have a few valid entries,
        the rest being empty.
        
        The `entries` property contains only live entries.
        There may be a `raw_entries` property that contains all
        allocated entries, used and unused.
        """
        return list()
    
    def file(self, i):
        """Return a string containing file bytes for entry at index i.
        
        Some containers may only wrap a single file, in this case
        the file has index 0.
        """
        raise FileNotFoundError
        
    def find(self, filename, ignore_case=False):
        """Return a string containing file bytes for the named entry.
        
        Some containers may only wrap a single file, in this case
        the name of that file is container-specfic, and should not
        be relied upon.
        
        Filenames are case-sensitive, unless `ignore_case` is 
        passed as `True`.
        """
        raise FileNotFoundError


# Entry formats are container-specific, as the entry will have properties
# needed by the container to be able to retreive the bytes for that entry.
# (For instance, a disk entry will contain the track/sector information.)
#
# The common properties are listed here.

class FileEntry(object):
    """Represents a single entry in a container, or a wrapped file.
    
    Entries may not know how to retreive their own data bytes.
    Typically the container is needed to be able to extract the bytes
    for a single entry.
    """
    
    @property
    def raw_name(self):
        """Name of this entry, as raw bytes from the container format.
        
        The `raw_name` of an entry is the actual bytes of the filename
        per the container file-format. This may include trailing spaces,
        trailing shift-spaces, or other format-specific bytes.
        
        Use `name` for a host-printable name.
        """
        pass
    
    @property
    def name(self):
        """Display name of this entry.
        
        The display name is based on the raw_name, but will have
        trailing spaces and shift-spaces stripped off.
        """
        pass
