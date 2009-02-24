class Program(object):
    """Represents a chunk of bytes to disassemble."""
    def __init__(self, start_address):
        self.blocks = list()
        self.start_address = start_address
        self.basic_listing = ""

    def addblock(self, block):
        self.blocks.append(block)
