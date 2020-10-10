"""CPU functionality."""

import sys
import datetime

# register psuedonyms
IM = 5  # interrupt mask
IS = 6  # interrupt status
SP = 7  # stack pointer

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
        # R5 is reserved as the interrupt mask (IM)
        self.reg[IM] = 0b00000001
        # R6 is reserved as the interrupt status (IS)
        # Register 7 is the stack pointer, 0xF4 means stack is empty
        self.reg[SP] = 0xF4
        # Program Counter - location of currently executing instruction in RAM
        self.pc = 0
        self.fl = 0             # flags - holds results of CMP instruction
        self.ram = [0] * 256

        self.interrupts_enabled = True

        self.clock_tick = datetime.datetime.now().second

    def ram_read(self, addr):
        if addr < len(self.ram):
            return self.ram[addr]
        else:
            raise Exception("Memory address out of range!")

    def ram_write(self, val, addr):
        if addr < len(self.ram):
            self.ram[addr] = val
        else:
            raise Exception("Memory address out of range!")

    def load(self):
        """Load a program into memory."""

        address = 0
        load_address = 0

        program = [0] * 256

        if len(sys.argv) != 2:
            print(f"Usage:\npython3 {sys.argv[0]} filename.ls8")
            exit()
        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    possible_num = line[:line.find('#')]    # strip comments
                    if possible_num == '':                  # strip blank lines
                        continue
                    # convert "binary" string into a number
                    program[load_address] = (int(possible_num, 2))
                    load_address += 1
                    if load_address == 256:
                        raise Exception("Out of memory. Program is too large.")

        except FileNotFoundError:
            print(f"{sys.argv[1]} not found.")
            exit()

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "AND":
            self.reg[reg_a] = self.reg[reg_a] & self.reg[reg_b]
        elif op == "CMP":
            """
            The flags register FL holds the current flags status. These flags can change based on the
            operands given to the CMP opcode.
            The register is made up of 8 bits. If a particular bit is set, that flag is "true".

            FL bits: 00000LGE

            L Less-than: during a CMP, set to 1 if registerA is less than registerB, zero otherwise.
            G Greater-than: during a CMP, set to 1 if registerA is greater than registerB, zero otherwise.
            E Equal: during a CMP, set to 1 if registerA is equal to registerB, zero otherwise.
            """

            if self.reg[reg_a] == self.reg[reg_b]:
                self.fl = 1
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.fl = 2
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.fl = 4
            else:
                raise Exception(
                    "CMP: Invalid inputs or error computing result")
        elif op == "DEC":
            self.reg[reg_a] -= 1
        elif op == "DIV":
            if self.reg[reg_b]:
                raise Exception("DIV: Division by zero")
            self.reg[reg_a] /= self.reg[reg_b]
        elif op == "INC":
            self.reg[reg_a] += 1
        elif op == "MOD":
            if self.reg[reg_b]:
                raise Exception("MOD: Division by zero")
            self.reg[reg_a] = self.reg[reg_a] % self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "NOT":
            self.reg[reg_a] = ~self.reg[reg_a]
        elif op == "OR":
            self.reg[reg_a] = self.reg[reg_a] | self.reg[reg_b]
        elif op == "SHL":
            self.reg[reg_a] = self.reg[reg_a] << self.reg[reg_b]
        elif op == "SHR":
            self.reg[reg_a] = self.reg[reg_a] >> self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "XOR":
            self.reg[reg_a] = self.reg[reg_a] ^ self.reg[reg_b]
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
            if self.interrupts_enabled:
                if datetime.datetime.now().second - self.clock_tick >= 1:
                    self.clock_tick = datetime.datetime.now().second
                    # issue the time interrupt
                    self.reg[IS] = self.reg[IS] | 0b00000001

            self.check_interrupts()

            """
            Meanings of the bits in the first byte of each instruction: AABCDDDD

            AA Number of operands for this opcode, 0-2
            B 1 if this is an ALU operation
            C 1 if this instruction sets the PC
            DDDD Instruction identifier
            """

            # read the byte at the program counter into the Instruction Register
            ir = self.ram_read(self.pc)
            # read the next two bytes in case the instruction needs to utilize them
            num_operands = ir >> 6
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if ir not in instr:
                raise Exception(f"Invlaid instruction {ir}. Terminating.")

            # Direct the CPU to follow the correct instruction
            if instr[ir] == "HLT":
                # HLT "halt" instruction, ends program
                exit()
            elif (ir >> 5) & 0b001:
                # this is an ALU instruction - transfer to ALU
                self.alu(instr[ir], operand_a, operand_b)
            elif num_operands == 0:
                # single byte instructions (no operands)
                getattr(self, instr[ir])()
            elif num_operands == 1:
                # two-bye (one operand) instructions
                getattr(self, instr[ir])(operand_a)
            elif num_operands == 2:
                # three-byte (two operand) instructions
                getattr(self, instr[ir])(operand_a, operand_b)

            # Move the Program Counter
            if ir >> 4 & 0b0001:
                # this instruction set the PC, so we won't move it.
                continue
            else:
                # move the PC forward by one + the number of operands used
                self.pc += num_operands + 1

    def check_interrupts(self):
        """
        There are 8 interrupts, I0-I7.

        When an interrupt occurs from an external source or from an INT instruction, the appropriate 
        bit in the IS register will be set.

        Prior to instruction fetch, the following steps occur:
        1. The IM register is bitwise AND-ed with the IS register and the results stored as `maskedInterrupts`.
        2. Each bit of `maskedInterrupts` is checked, starting from 0 and going up to the 7th bit, one for each
            interrupt.
        3. If a bit is found to be set, follow the next sequence of steps. Stop further checking of 
            `maskedInterrupts`.

        If a bit is set:
        1. Disable further interrupts.
        2. Clear the bit in the IS register.
        3. The PC register is pushed on the stack.
        4. The FL register is pushed on the stack.
        5. Registers R0-R6 are pushed on the stack in that order.
        6. The address (vector in interrupt terminology) of the appropriate handler is looked up from
            the interrupt vector table.
        7. Set the PC is set to the handler address.
        """

        maskedInterrupts = self.reg[IM] & self.reg[IS]

        for i in range(8):
            check = 1 << i
            if maskedInterrupts & check:
                # Disable further interrupts
                self.interrupts_enabled = False

                # Clear the bit in the IS register
                self.reg[IS] = self.reg[IS] ^ check

                # push PC
                self.reg[SP] -= 1
                self.ram_write(self.pc, self.reg[SP])
                # push FL
                self.reg[SP] -= 1
                self.ram_write(self.fl, self.reg[SP])
                # push registers 0 - 6
                for r in range(7):
                    self.PUSH(r)

                # set PC to interrupt handler vector
                # (vector table starts at 0xF8 in RAM)
                self.pc = self.ram_read(0xF8 + i)

                # stop further checking of maskedInterrupts
                break

    # Implementation of non-ALU instructions handlers
    def CALL(self, reg):
        """
        Calls a subroutine (function) at the address stored in the register.

        1. The address of the instruction directly after CALL is pushed onto the stack. This allows
           us to return to where we left off when the subroutine finishes executing.
        2. The PC is set to the address stored in the given register. We jump to that location in
           RAM and execute the first instruction in the subroutine. The PC can move forward or backwards
           from its current location.
        """

        # PUSH
        self.reg[SP] -= 1
        self.ram_write(self.pc + 2, self.reg[SP])

        # Set PC to address in the given reg
        self.pc = self.reg[reg]

    def INT(self, reg):
        """
        Issue the interrupt number stored in the given register.
        This will set the _n_th bit in the IS register to the value in the given register.
        R6 is reserved as the interrupt status (IS)
        """
        interrupt_num = self.reg[reg]   # get the number of the interrupt from the given register
        if interrupt_num < 0 or interrupt_num > 7:
            raise Exception(
                f"INT: Invalid interrupt provided: {interrupt_num}")

        # set the appropriate bit for the requested interrupt
        self.reg[IS] = self.reg[IS] | (0b1 << interrupt_num)

    def IRET(self):
        """
        1. Registers R6-R0 are popped off the stack in that order.
        2. The FL register is popped off the stack.
        3. The return address is popped off the stack and stored in PC.
        4. Interrupts are re-enabled
        """

        for r in range(6, -1, -1):
            # pop off values for the states of the six registers that existed
            # before the interrupt handler was called
            self.reg[r] = self.ram_read(self.reg[SP])
            self.reg[SP] += 1

        self.fl = self.ram_read(self.reg[SP])   # pop off FL
        self.reg[SP] += 1
        self.pc = self.ram_read(self.reg[SP])   # pop off PC
        self.reg[SP] += 1

        self.interrupts_enabled = True

    def JEQ(self, reg):
        """
        If equal flag is set (true), jump to the address stored in the given register.
        """
        if self.fl & 1:
            self.JMP(reg)
        else:
            self.pc += 2

    def JGE(self, reg):
        """
        If greater-than flag or equal flag is set (true), jump to the address stored in the given register.
        """

        if self.fl & 1 or self.fl & 0b10:
            self.JMP(reg)
        else:
            self.pc += 2

    def JGT(self, reg):
        """
        If greater-than flag is set (true), jump to the address stored in the given register.
        """

        if self.fl & 0b10:
            self.JMP(reg)
        else:
            self.pc += 2

    def JLE(self, reg):
        """
        If less-than flag or equal flag is set (true), jump to the address stored in the given register.
        """

        if self.fl & 1 or self.fl & 0b100:
            self.JMP(reg)
        else:
            self.pc += 2

    def JLT(self, reg):
        """
        If less-than flag is set (true), jump to the address stored in the given register.
        """

        if self.fl & 0b100:
            self.JMP(reg)
        else:
            self.pc += 2

    def JMP(self, reg):
        """
        Jump (set the PC) to the address stored in the given register.
        """
        self.pc = self.reg[reg]

    def JNE(self, reg):
        """
        If equal flag is clear (false, 0), jump to the address stored in the given register.
        """

        if not self.fl & 1:
            self.JMP(reg)
        else:
            self.pc += 2

    def LD(self, reg_a, reg_b):
        raise Exception("Instruction not yet implemented: LD")

    def LDI(self, reg, val):
        # Load immediate value into a register
        if reg >= 0 and reg <= 7:
            self.reg[reg] = val
        else:
            raise Exception(f"Invalid register requested for LDI: {reg}")

    def NOP(self):
        """ Do nothing """
        pass

    def POP(self, reg):
        """
        Pop the value at the top of the stack into the given register.
        1. Copy the value from the address pointed to by SP to the given register.
        2. Increment SP.
        """
        self.reg[reg] = self.ram_read(self.reg[SP])
        self.reg[SP] += 1

    def PRA(self, reg):
        """
        Print alpha character value stored in the given register.
        Print to the console the ASCII character corresponding to the value in the register.
        """

        print(chr(self.reg[reg]))

    def PRN(self, reg):
        """
        Print to the console the decimal integer value that is stored in the given register.
        """
        if reg >= 0 and reg <= 7:    # should this be 4 since 5,6,7 are reserved?
            print(self.reg[reg])
        else:
            raise Exception(f"Invalid register requested for PRN: {reg}")

    def PUSH(self, reg):
        """
        Push the value in the given register on the stack.
        1. Decrement the SP.
        2. Copy the value in the given register to the address pointed to by SP.
        """
        self.reg[SP] -= 1
        self.ram_write(self.reg[reg], self.reg[SP])

    def RET(self):
        """
        Return from subroutine.
        Pop the value from the top of the stack and store it in the PC.
        """

        # POP
        self.pc = self.ram_read(self.reg[SP])
        self.reg[SP] += 1

    def ST(self, reg_a, reg_b):
        """
        Store value in reg_b into the address stored in reg_a
        """
        self.ram_write(self.reg[reg_b], self.reg[reg_a])
