"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    # Static instructions
    HLT = 0b00000001
    PRN = 0b01000111
    LDI = 0b10000010
    MUL = 0b10100010
    PUSH = 0b01000101
    POP = 0b01000110
    CALL = 0b01010000
    RET = 0b00010001
    ADD = 0b10100000

    # Static registers
    SP = 7

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.reg[self.SP] = 0xf4
        self.instructions = {
            self.PRN: self.print_instruction,
            self.LDI: self.load_instruction,
            self.MUL: self.multiply,
            self.PUSH: self.push,
            self.POP: self.pop,
            self.CALL: self.call,
            self.RET: self.ret,
            self.ADD: self.add
        }

    def load(self, program_file):
        """Load a program into memory."""

        address = 0

        with open(program_file) as f:
            for line in f:
                line = line.split('#')
                line = line[0].strip()

                if line == '':
                    continue

                self.ram[address] = int(line, 2)
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def print_instruction(self, a, b):
        print(self.reg[a])
        self.pc += 2

    def load_instruction(self, a, b):
        self.reg[a] = b
        self.pc += 3

    def multiply(self, a, b):
        self.reg[a] *= self.reg[b]
        self.pc += 3

    def push(self, a, b):
        self.reg[self.SP] -= 1
        self.ram[self.reg[self.SP]] = self.reg[a]
        self.pc += 2

    def pop(self, a, b):
        self.reg[a] = self.ram[self.reg[self.SP]]
        self.reg[self.SP] += 1
        self.pc += 2

    def call(self, a, b):
        self.reg[self.SP] -= 1
        self.ram[self.reg[self.SP]] = self.pc + 2
        self.pc = self.reg[a]

    def ret(self, a, b):
        self.pc = self.ram[self.reg[self.SP]]
        self.reg[self.SP] += 1

    def add(self, a, b):
        self.reg[a] += self.reg[b]
        self.pc += 3

    def run(self):
        """Run the CPU."""
        while True:
            #print(self.pc)
            ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if ir == self.HLT:
                break
            else:
                self.instructions[ir](operand_a, operand_b)
