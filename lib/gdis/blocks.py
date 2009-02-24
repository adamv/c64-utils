class Address(object):
    def __init__(self, addr):
        self.addr = addr
        self.label = None
        
    def __str__(self):
        if self.label:
            return "%s; $%04X" % (self.label, self.addr)
        else:
            return "$%04X" % (self.addr)
            
    def __repr__(self):
        return "<Address $%04X %s>" % (self.addr, self.label)
        
    def __int__(self):
        return self.addr


class DisassemblyBlock(object):
    def pull_labels(self, symbols):
        """Pull labels from `symbols` that apply to this block.
        
        This method allows a derived class to scan for symbols.
        """
        pass


class Instruction(DisassemblyBlock):
    def __init__(self, address, opcode, operand):
        self.address = Address(address)
        self.opcode = opcode
        self.operand = Address(operand)

    def __str__(self):
        return "%s    %s" % (self.address, self.opcode.write(self.operand))

    def pull_labels(self, symbols):
        if self.opcode.bytes != 3:
            return
            
        for s in symbols:
            if s[1] == self.operand.addr:
                self.operand.label = s[0]
                return


class Comment(DisassemblyBlock):
    def __init__(self, address, comment):
        self.address = Address(address)
        self.comment = comment
        
    def __str__(self):
        return '; '+self.comment


class AsciiData(DisassemblyBlock):
    def __init__(self, address, bytes):
        self.address = Address(address)
        self.bytes = bytes
        
    def __len__(self):
        return len(self.bytes)

    def __str__(self):
        return "$%04X .ascii \"%s\"" % (self.address, self.bytes)


class DataByte(DisassemblyBlock):
    def __init__(self, address, byte):
        self.address = Address(address)
        self.byte = byte
        
    def __str__(self):
        return "$%04X .byte $%02X" % (self.address, self.byte)
