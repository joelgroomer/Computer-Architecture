"""CPU functionality."""

import sys

# instruction psuedonyms
instr = {
    0b10100000: "ADD",
    0b10101000: "AND",
    0b01010000: "CALL",
    0b10100111: "CMP",
    0b01100110: "DEC",
    0b10100011: "DIV",
    0b00000001: "HLT",
    0b01100101: "INC",
    0b01010010: "INT",
    0b00010011: "IRET",
    0b01010101: "JEQ",
    0b01011010: "JGE",
    0b01010111: "JGT",
    0b01011001: "JLE",
    0b01011000: "JLT",
    0b01010100: "JMP",
    0b01010110: "JNE",
    0b10000011: "LD",
    0b10000010: "LDI",
    0b10100100: "MOD",
    0b10100010: "MUL",
    0b00000000: "NOP",
    0b01101001: "NOT",
    0b10101010: "OR",
    0b01000110: "POP",
    0b01001000: "PRA",
    0b01000111: "PRN",
    0b01000101: "PUSH",
    0b00010001: "RET",
    0b10101100: "SHL",
    0b10101101: "SHR",
    0b10000100: "ST",
    0b10100001: "SUB",
    0b10101011: "XOR"
}


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        # Register 7 is the stack pointer, 0xF4 means stack is empty
        self.reg[7] = 0xF4
        self.pc = 0
        self.fl = 0
        self.ram = [0] * 256

    def ram_read(self, addr):
        if addr < len(self.ram):
            return self.ram[addr]
        return None

    def ram_write(self, val, addr):
        if addr < len(self.ram):
            self.ram[addr] = val

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "AND":
            raise Exception("Instruction not yet implemented: AND")
        elif op == "CMP":
            raise Exception("Instruction not yet implemented: CMP")
        elif op == "DEC":
            raise Exception("Instruction not yet implemented: DEC")
        elif op == "DIV":
            raise Exception("Instruction not yet implemented: DIV")
        elif op == "INC":
            raise Exception("Instruction not yet implemented: INC")
        elif op == "MOD":
            raise Exception("Instruction not yet implemented: MOD")
        elif op == "MUL":
            raise Exception("Instruction not yet implemented: MUL")
        elif op == "NOT":
            raise Exception("Instruction not yet implemented: NOT")
        elif op == "OR":
            raise Exception("Instruction not yet implemented: OR")
        elif op == "SHL":
            raise Exception("Instruction not yet implemented: SHL")
        elif op == "SHR":
            raise Exception("Instruction not yet implemented: SHR")
        elif op == "SUB":
            raise Exception("Instruction not yet implemented: SUB")
        elif op == "XOR":
            raise Exception("Instruction not yet implemented: XOR")
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        running = True
        while running:
            # read the byte at the program counter into the Instruction Register
            ir = self.ram_read(self.pc)
            # read the next two bytes in case the instruction
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)  # ...needs to utilize them

            if ir not in instr:
                raise Exception(f"Invlaid instruction {ir}. Terminating.")

            # Direct the CPU to follow the correct instruction
            if ir == 1:
                # HLT "halt" instruction, ends program
                exit()
            elif ir & 0b00100000 == 32:
                # this is an ALU instruction - transfer to ALU
                self.alu(instr[ir], operand_a, operand_b)
            elif ir & 0b11000000 == 0:
                # single byte instructions (no operands)
                getattr(self, instr[ir])()
            elif ir & 0b11000000 == 64:
                # two-bye (one operand) instructions
                getattr(self, instr[ir])(operand_a)
            elif ir & 0b11000000 == 128:
                # three-byte (two operand) instructions
                getattr(self, instr[ir])(operand_a, operand_b)

            # Move the Program Counter
            if ir & 0b00010000 == 16:
                # this instruction set the PC, so we won't move it.
                continue
            elif ir & 0b11000000 == 0:
                # single byte instructions (no operands)
                self.pc += 1
            elif ir & 0b11000000 == 64:
                # two-bye (one operand) instructions
                self.pc += 2
            elif ir & 0b11000000 == 128:
                # three-byte (two operand) instructions
                self.pc += 3

    # Implementation of non-ALU instructions
    def CALL(self):
        raise Exception("Instruction not yet implemented: CALL")

    def INT(self):
        raise Exception("Instruction not yet implemented: INT")

    def IRET(self):
        raise Exception("Instruction not yet implemented: IRET")

    def JEQ(self):
        raise Exception("Instruction not yet implemented: JEQ")

    def JGE(self):
        raise Exception("Instruction not yet implemented: JGE")

    def JGT(self):
        raise Exception("Instruction not yet implemented: JGT")

    def JLE(self):
        raise Exception("Instruction not yet implemented: JLE")

    def JLT(self):
        raise Exception("Instruction not yet implemented: JLT")

    def JMP(self):
        raise Exception("Instruction not yet implemented: JMP")

    def JNE(self):
        raise Exception("Instruction not yet implemented: JNE")

    def LD(self):
        raise Exception("Instruction not yet implemented: LD")

    def LDI(self):
        raise Exception("Instruction not yet implemented: LDI")

    def NOP(self):
        raise Exception("Instruction not yet implemented: NOP")

    def POP(self):
        raise Exception("Instruction not yet implemented: POP")

    def PRA(self):
        raise Exception("Instruction not yet implemented: PRA")

    def PRN(self):
        raise Exception("Instruction not yet implemented: PRN")

    def PUSH(self):
        raise Exception("Instruction not yet implemented: PUSH")

    def RET(self):
        raise Exception("Instruction not yet implemented: RET")

    def ST(self):
        raise Exception("Instruction not yet implemented: ST")
