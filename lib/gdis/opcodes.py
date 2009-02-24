
class OpCode(object):
    def __init__(self, *parts):
        self.name, self.opcode, self.bytes, self.syntax = parts

    def __str__(self):
        return self.define()
        
    def format_operand(self, operand):
        if self.bytes == 2:
            return '$%02X' % (operand)
        elif self.bytes == 3:
            return '$%04X' % (operand)
        else:
            return ''
        
    def write(self, operand):
        if '*' not in self.syntax:
            return self.name
            
        f = self.syntax.replace('*', self.format_operand(operand))
        l = '; '+operand.label if operand.label else ''
        return '%s %s %s' % (self.name, f, l)
    
    def read_operand(self, r):
        if self.bytes == 2:
            return r.byte()
        elif self.bytes == 3:
            return r.word()
        else:
            return None
    
    def read(self, r):
        return self.write(self.read_operand(r))
        
    def define(self):
        return '%s %02X %d %s' % (self.name, self.opcode, self.bytes, self.syntax)
        
    def __repr__(self):
        return '<OpCode %s>' % self.define()

opcodes = (
    OpCode("ADC", 0x69, 2, "#*"), 
    OpCode("ADC", 0x61, 2, "(*,X)"), 
    OpCode("ADC", 0x71, 2, "(*),Y"), 
    OpCode("ADC", 0x7D, 3, "*,X"), 
    OpCode("ADC", 0x79, 3, "*,Y"), 
    OpCode("ADC", 0x6D, 3, "*"), 
    OpCode("AND", 0x29, 2, "#*"), 
    OpCode("AND", 0x21, 2, "(*,X)"), 
    OpCode("AND", 0x31, 2, "(*),Y"), 
    OpCode("AND", 0x3D, 3, "*,X"), 
    OpCode("AND", 0x39, 3, "*,Y"), 
    OpCode("AND", 0x2D, 3, "*"), 
    OpCode("ASL", 0x0A, 1, ""), 
    OpCode("ASL", 0x1E, 3, "*,X"), 
    OpCode("ASL", 0x0E, 3, "*"), 
    OpCode("BCC", 0x90, 2, "*"), 
    OpCode("BCS", 0xB0, 2, "*"), 
    OpCode("BEQ", 0xF0, 2, "*"), 
    OpCode("BMI", 0x30, 2, "*"), 
    OpCode("BNE", 0xD0, 2, "*"), 
    OpCode("BPL", 0x10, 2, "*"), 
    OpCode("BVC", 0x50, 2, "*"), 
    OpCode("BVS", 0x70, 2, "*"), 
    OpCode("BIT", 0x2C, 3, "*"), 
#    OpCode("BRK", 0x00, 1, ""), 
    OpCode("CLC", 0x18, 1, ""), 
    OpCode("CLD", 0xD8, 1, ""), 
    OpCode("CLI", 0x58, 1, ""), 
    OpCode("CLV", 0xB8, 1, ""), 
    OpCode("CMP", 0xC9, 2, "#*"), 
    OpCode("CMP", 0xC1, 2, "(*,X)"), 
    OpCode("CMP", 0xD1, 2, "(*),Y"), 
    OpCode("CMP", 0xDD, 3, "*,X"), 
    OpCode("CMP", 0xD9, 3, "*,Y"), 
    OpCode("CMP", 0xCD, 3, "*"), 
    OpCode("CPX", 0xE0, 2, "#*"), 
    OpCode("CPX", 0xEC, 3, "*"), 
    OpCode("CPY", 0xC0, 2, "#*"), 
    OpCode("CPY", 0xCC, 3, "*"), 
    OpCode("DEC", 0xDE, 3, "*,X"), 
    OpCode("DEC", 0xCE, 3, "*"), 
    OpCode("DEX", 0xCA, 1, ""), 
    OpCode("DEY", 0x88, 1, ""), 
    OpCode("EOR", 0x49, 2, "#*"), 
    OpCode("EOR", 0x41, 2, "(*,X)"), 
    OpCode("EOR", 0x51, 2, "(*),Y"), 
    OpCode("EOR", 0x5D, 3, "*,X"), 
    OpCode("EOR", 0x59, 3, "*,Y"), 
    OpCode("EOR", 0x4D, 3, "*"), 
    OpCode("INC", 0xFE, 3, "*,X"), 
    OpCode("INC", 0xEE, 3, "*"), 
    OpCode("INX", 0xE8, 1, ""), 
    OpCode("INY", 0xC8, 1, ""), 
    OpCode("JMP", 0x6C, 3, "(*)"), 
    OpCode("JMP", 0x4C, 3, "*"), 
    OpCode("JSR", 0x20, 3, "*"),
    
    OpCode("LDA", 0xA9, 2, "#*"), 
    OpCode("LDA", 0xA1, 2, "(*,X)"), 
    OpCode("LDA", 0xB1, 2, "(*),Y"), 
    OpCode("LDA", 0xBD, 3, "*,X"), 
    OpCode("LDA", 0xB9, 3, "*,Y"), 
    OpCode("LDA", 0xAD, 3, "*"),
    OpCode("LDA", 0xA5, 2, "*"),
    
    OpCode("LDX", 0xA2, 2, "#*"), 
    OpCode("LDX", 0xBE, 3, "*,Y"), 
    OpCode("LDX", 0xAE, 3, "*"), 
    OpCode("LDX", 0xA6, 2, "*"), 
    
    OpCode("LDY", 0xA0, 2, "#*"), 
    OpCode("LDY", 0xBC, 3, "*,X"), 
    OpCode("LDY", 0xAC, 3, "*"),
    OpCode("LDY", 0xA4, 2, "*"),
    
    OpCode("LSR", 0x4A, 1, ""), 
    OpCode("LSR", 0x5E, 3, "*,X"), 
    OpCode("LSR", 0x4E, 3, "*"), 
    OpCode("NOP", 0xEA, 1, ""), 
    OpCode("ORA", 0x09, 2, "#*"), 
    OpCode("ORA", 0x01, 2, "(*,X)"), 
    OpCode("ORA", 0x11, 2, "(*),Y"), 
    OpCode("ORA", 0x1D, 3, "*,X"), 
    OpCode("ORA", 0x19, 3, "*,Y"), 
    OpCode("ORA", 0x0D, 3, "*"), 
    OpCode("ORA", 0x05, 2, "*"), 
    OpCode("PHA", 0x48, 1, ""), 
    OpCode("PHP", 0x08, 1, ""), 
    OpCode("PLA", 0x68, 1, ""), 
    OpCode("PLP", 0x28, 1, ""), 
    OpCode("ROL", 0x2A, 1, ""), 
    OpCode("ROL", 0x3E, 3, "*,X"), 
    OpCode("ROL", 0x2E, 3, "*"),
    OpCode("ROL", 0x26, 2, "*"),
    OpCode("ROR", 0x6A, 1, ""), 
    OpCode("ROR", 0x7E, 3, "*,X"), 
    OpCode("ROR", 0x6E, 3, "*"), 
    OpCode("RTI", 0x40, 1, ""), 
    OpCode("RTS", 0x60, 1, ""), 
    OpCode("SBC", 0xE9, 2, "#*"), 
    OpCode("SBC", 0xE1, 2, "(*,X)"), 
    OpCode("SBC", 0xF1, 2, "(*),Y"), 
    OpCode("SBC", 0xFD, 3, "*,X"), 
    OpCode("SBC", 0xF9, 3, "*,Y"), 
    OpCode("SBC", 0xED, 3, "*"), 
    OpCode("SEC", 0x38, 1, ""), 
    OpCode("SED", 0xF8, 1, ""), 
    OpCode("SEI", 0x78, 1, ""), 
    OpCode("STA", 0x81, 2, "(*,X)"), 
    OpCode("STA", 0x91, 2, "(*),Y"), 
    OpCode("STA", 0x9D, 3, "*,X"), 
    OpCode("STA", 0x99, 3, "*,Y"), 
    OpCode("STA", 0x8D, 3, "*"), 
    OpCode("STA", 0x85, 2, "*"), 

    OpCode("STX", 0x96, 2, "*,Y"), 
    OpCode("STX", 0x8E, 3, "*"), 
    OpCode("STX", 0x84, 2, "*"), 

    OpCode("STY", 0x94, 2, "*,X"), 
    OpCode("STY", 0x8C, 3, "*"), 
    OpCode("STY", 0x95, 2, "*"), 

    OpCode("TAX", 0xAA, 1, ""), 
    OpCode("TAY", 0xA8, 1, ""), 
    OpCode("TSX", 0xBA, 1, ""), 
    OpCode("TXA", 0x8A, 1, ""), 
    OpCode("TXS", 0x9A, 1, ""), 
    OpCode("TYA", 0x98, 1, "")
)

op_map = dict( (o.opcode, o) for o in opcodes )
