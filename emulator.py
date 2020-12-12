from io import BytesIO
from typing import IO, Optional
import random


class Emulator:

    MOD_4_BIT = 0x10
    MOD_8_BIT = 0x100
    PROGRAM_START = 0x200
    STACK_SIZE = 16
    MEMORY_SIZE = 0xFFF
    V_REGISTER_COUNT = 16
    FONT_SIZE = 5

    FONTS = [
        [0xF0, 0x90, 0x90, 0x90, 0xF0],  # 0 @ 0x00 - 0x04
        [0x20, 0x60, 0x20, 0x20, 0x70],  # 1 @ 0x05 - 0x09
        [0xF0, 0x10, 0xF0, 0x80, 0xF0],  # 2 @ 0x0A - 0x0E
        [0xF0, 0x10, 0xF0, 0x10, 0xF0],  # 3 @ 0x0F - 0x13
        [0x90, 0x90, 0xF0, 0x10, 0x10],  # 4 @ 0x14 - 0x19
        [0xF0, 0x80, 0xF0, 0x10, 0xF0],  # 5 @ 0x1A - 0x1E
        [0xF0, 0x80, 0xF0, 0x90, 0xF0],  # 6 @ 0x1F - 0x23
        [0xF0, 0x10, 0x20, 0x40, 0x40],  # 7 @ 0x24 - 0x29
        [0xF0, 0x90, 0xF0, 0x90, 0xF0],  # 8 @ 0x2A - 0x2E
        [0xF0, 0x90, 0xF0, 0x10, 0xF0],  # 9 @ 0x2F - 0x33
        [0xF0, 0x90, 0xF0, 0x90, 0x90],  # A @ 0x34 - 0x39
        [0xE0, 0x90, 0xE0, 0x90, 0xE0],  # B @ 0x3A - 0x3E
        [0xF0, 0x80, 0x80, 0x80, 0xF0],  # C @ 0x3F - 0x43
        [0xE0, 0x90, 0x90, 0x90, 0xE0],  # D @ 0x44 - 0x49
        [0xF0, 0x80, 0xF0, 0x80, 0xF0],  # E @ 0x4A - 0x4E
        [0xF0, 0x80, 0xF0, 0x80, 0x80]   # F @ 0x4F - 0x53
    ]

    INSTRUCTION_TABLE = {
        (0x00E0, 0xFFFF): lambda e, op: e.cls(),
        (0x00EE, 0xFFFF): lambda e, op: e.ret(),
        (0x0000, 0xF000): lambda e, op: e.sys_address(op & 0x0FFF),
        (0x1000, 0xF000): lambda e, op: e.jp_address(op & 0x0FFF),
        (0x2000, 0xF000): lambda e, op: e.call_address(op & 0xFFF),
        (0x3000, 0xF000): lambda e, op: e.se_v_byte((op & 0x0F00) >> 8, op & 0x00FF),
        (0x4000, 0xF000): lambda e, op: e.sne_v_byte((op & 0x0F00) >> 8, op & 0x00FF),
        (0x5000, 0xF00F): lambda e, op: e.se_v_v((op & 0x0F00) >> 8, (op & 0x00F0) >> 4),
        (0x6000, 0xF000): lambda e, op: e.ld_v_byte((op & 0x0F00) >> 8, op & 0x00FF),
        (0x7000, 0xF000): lambda e, op: e.add_v_byte((op & 0x0F00) >> 8, op & 0x00FF),
        (0x8000, 0xF00F): lambda e, op: e.ld_v_v((op & 0x0F00) >> 8, (op & 0x00F0) >> 4),
        (0x8001, 0xF00F): lambda e, op: e.or_v_v((op & 0x0F00) >> 8, (op & 0x00F0) >> 4),
        (0x8002, 0xF00F): lambda e, op: e.and_v_v((op & 0x0F00) >> 8, (op & 0x00F0) >> 4),
        (0x8003, 0xF00F): lambda e, op: e.xor_v_v((op & 0x0F00) >> 8, (op & 0x00F0) >> 4),
        (0x8004, 0xF00F): lambda e, op: e.add_v_v((op & 0x0F00) >> 8, (op & 0x00F0) >> 4),
        (0x8005, 0xF00F): lambda e, op: e.sub_v_v((op & 0x0F00) >> 8, (op & 0x00F0) >> 4),
        (0x8006, 0xF00F): lambda e, op: e.shr_v((op & 0x0F00) >> 8),
        (0x8007, 0xF00F): lambda e, op: e.subn_v_v((op & 0x0F00) >> 8, (op & 0x00F0) >> 4),
        (0x800E, 0xF00F): lambda e, op: e.shl_v((op & 0x0F00) >> 8),
        (0x9000, 0xF00F): lambda e, op: e.sne_v_v((op & 0x0F00) >> 8, (op & 0x00F0) >> 4),
        (0xA000, 0xF000): lambda e, op: e.ld_i_address(op & 0x0FFF),
        (0xB000, 0xF000): lambda e, op: e.jp_v0_address(op & 0x0FFF),
        (0xC000, 0xF000): lambda e, op: e.rnd_v_byte((op & 0x0F00) >> 8, op & 0x00FF),
        (0xD000, 0xF000): lambda e, op: e.drw((op & 0x0F00) >> 8, (op & 0x00F0) >> 4, op & 0x000F),
        (0xE09E, 0xF0FF): lambda e, op: e.skp_v((op & 0x0F00) >> 8),
        (0xE0A1, 0xF0FF): lambda e, op: e.sknp_v((op & 0x0F00) >> 8),
        (0xF007, 0xF0FF): lambda e, op: e.ld_v_dt((op & 0x0F00) >> 8),
        (0xF00A, 0xF0FF): lambda e, op: e.ld_v_k((op & 0x0F00) >> 8),
        (0xF015, 0xF0FF): lambda e, op: e.ld_dt_v((op & 0x0F00) >> 8),
        (0xF018, 0xF0FF): lambda e, op: e.ld_st_v((op & 0x0F00) >> 8),
        (0xF01E, 0xF0FF): lambda e, op: e.add_i_v((op & 0x0F00) >> 8),
        (0xF029, 0xF0FF): lambda e, op: e.ld_f_v((op & 0x0F00) >> 8),
        (0xF033, 0xF0FF): lambda e, op: e.ld_b_v((op & 0x0F00) >> 8),
        (0xF055, 0xF0FF): lambda e, op: e.ld_i_v((op & 0x0F00) >> 8),
        (0xF065, 0xF0FF): lambda e, op: e.ld_v_i((op & 0x0F00) >> 8),
    }

    def __init__(self, source: Optional[BytesIO]):
        self.v_registers = [0] * Emulator.V_REGISTER_COUNT
        self.i_register = 0
        self.dt_register = 0
        self.st_register = 0
        self.stack_pointer = 0
        self.memory = bytearray(Emulator.MEMORY_SIZE)
        self.stack = [0] * Emulator.STACK_SIZE
        self.program_counter = Emulator.PROGRAM_START
        self.display = Emulator.empty_display()
        self.pixels_to_update = []
        self.wait_for_keypress = False
        self.store_keypress_in_v = None
        self.keys_pressed = []

        Emulator._init_fonts(self.memory)

        if source is not None:
            Emulator._read_source(source, self.memory, self.program_counter)

    def next(self) -> bool:
        self.pixels_to_update = []
        if self.program_counter < len(self.memory):
            opcode = int.from_bytes(self.memory[self.program_counter:self.program_counter + 2], 'big')
            self._execute(opcode)
            return True
        else:
            return False

    def _execute(self, opcode: int) -> None:
        for (pattern, mask), instruction in Emulator.INSTRUCTION_TABLE.items():
            if not (opcode ^ pattern) & mask:
                jump = instruction(self, opcode)
                # Jumps are handled by their respective instructions
                if not jump:
                    self.increment_program_counter()

    def cls(self) -> None:
        self.display = Emulator.empty_display()

    def ret(self) -> bool:  # TODO unit test
        self.program_counter = self.stack[self.stack_pointer]
        self.stack_pointer = (self.stack_pointer - 1) % Emulator.MOD_4_BIT
        return True

    def sys_address(self, address: int) -> None:
        """Unused"""
        pass

    def jp_address(self, address: int) -> bool:
        """
        Moves the program counter to the specified address. Note:
        Programs start at 0x200. However, there is nothing stopping
        programs from jumping to <0x200 addresses. Have fun executing
        font data.
        :param address: A value in the range [0, 0xFFF]
        :return: True, since we are jumping
        """
        self.program_counter = address
        return True

    def call_address(self, address: int) -> bool:  # TODO unit test
        self.stack_pointer = (self.stack_pointer + 1) % Emulator.MOD_4_BIT
        self.stack[self.stack_pointer] = self.program_counter
        self.program_counter = address
        return True

    def se_v_byte(self, vx: int, byte: int) -> bool:  # TODO unit test
        if self.v_registers[vx] == byte:
            self.increment_program_counter(2)
            return True
        return False

    def sne_v_byte(self, vx: int, byte: int) -> bool:  # TODO unit test
        if self.v_registers[vx] != byte:
            self.increment_program_counter(2)
            return True
        return False

    def se_v_v(self, vx: int, vy: int) -> bool:  # TODO unit test
        if self.v_registers[vx] == self.v_registers[vy]:
            self.increment_program_counter(2)
            return True
        return False

    def ld_v_byte(self, vx: int, byte: int) -> None:
        self.v_registers[vx] = byte

    def add_v_byte(self, vx: int, byte: int) -> None:
        """
        Add Vx and a byte together and store the result in Vx. Since
        registers are only 8-bit, mod the result to the range [0, 0xFF].
        :param vx: The "x" in Vx
        :param byte: An 8-bit value
        """
        self.v_registers[vx] = (self.v_registers[vx] + byte) % Emulator.MOD_8_BIT

    def ld_v_v(self, vx: int, vy: int) -> None:
        self.v_registers[vx] = self.v_registers[vy]

    def or_v_v(self, vx: int, vy: int) -> None:
        self.v_registers[vx] |= self.v_registers[vy]

    def and_v_v(self, vx: int, vy: int) -> None:
        self.v_registers[vx] &= self.v_registers[vy]

    def xor_v_v(self, vx: int, vy: int) -> None:
        self.v_registers[vx] ^= self.v_registers[vy]

    def add_v_v(self, vx: int, vy: int) -> None:
        """
        Add Vx and Vy together and store the result in Vx. Since
        registers are only 8-bit, mod the result in range [0, 255]
        :param vx: The "x" in Vx
        :param vy: The "y" in Vy
        """
        self.v_registers[vx] = (self.v_registers[vx] + self.v_registers[vy]) % Emulator.MOD_8_BIT

    def sub_v_v(self, vx: int, vy: int) -> None:
        """
        TODO unit test
        :param vx:
        :param vy:
        :return:
        """
        self.v_registers[0xF] = 1 if self.v_registers[vx] > self.v_registers[vy] else 0
        self.v_registers[vx] = (self.v_registers[vx] - self.v_registers[vy]) % Emulator.MOD_8_BIT

    def shr_v(self, vx: int) -> None:
        """
        TODO unit test
        :param vx:
        :return:
        """
        self.v_registers[0xF] = self.v_registers[vx] & 0x1
        self.v_registers[vx] >>= 1

    def subn_v_v(self, vx: int, vy: int) -> None:
        """
        Set Vx = Vy - Vx, set VF = NOT borrow.
        If Vy > Vx, then VF is set to 1, otherwise 0.
        Then Vx is subtracted from Vy, and the results stored in Vx.
        TODO unit test
        """
        self.v_registers[0xF] = 1 if self.v_registers[vy] > self.v_registers[vx] else 0
        self.v_registers[vx] = (self.v_registers[vy] - self.v_registers[vx]) % Emulator.MOD_8_BIT

    def shl_v(self, vx: int) -> None:
        """
        If Vx has a 1 in the significant place, set VF to 1, otherwise 0.
        Bit-shift Vx left by 1. Mod the result to the range [0, 255].
        """
        self.v_registers[0xF] = (self.v_registers[vx] & 0x80) >> 7
        self.v_registers[vx] = (self.v_registers[vx] << 1) % Emulator.MOD_8_BIT

    def sne_v_v(self, vx: int, vy: int) -> bool:
        if self.v_registers[vx] != self.v_registers[vy]:
            self.program_counter += 2
            return True
        return False

    def ld_i_address(self, address: int) -> None:
        self.i_register = address

    def jp_v0_address(self, address: int) -> None:
        self.program_counter = self.v_registers[0] + address

    def rnd_v_byte(self, vx: int, byte: int) -> None:
        self.v_registers[vx] = random.randint(0, 255) & byte

    def drw(self, vx: int, vy: int, height: int) -> None:  # TODO unit test
        for row in range(height):
            sprite = self.memory[self.i_register + row]
            for col in range(8):
                x = (self.v_registers[vx] + col) % 64
                y = (self.v_registers[vy] + row) % 32
                sprite_pixel = bool(sprite & (0x80 >> col))
                current = self.display[y][x]
                # We don't want to draw to the entire display every time,
                # so add this pixel to the buffer
                if current != sprite_pixel:
                    self.pixels_to_update.append((x, y, sprite_pixel))
                if current and sprite_pixel:
                    self.v_registers[0xF] = True  # collision
                self.display[y][x] = current ^ sprite_pixel

    def skp_v(self, vx: int) -> bool:
        """
        Skip next instruction if key with code in Vx is pressed.
        """
        if self.v_registers[vx] in self.keys_pressed:
            self.increment_program_counter(2)
            return True
        else:
            return False

    def sknp_v(self, vx: int):  # TODO unit test
        if self.v_registers[vx] not in self.keys_pressed:
            self.increment_program_counter(2)
            return True
        else:
            return False

    def ld_v_dt(self, vx: int) -> None:
        self.v_registers[vx] = self.dt_register

    def ld_v_k(self, vx: int) -> None:
        """
        Wait for a keypress. Store the next keypress in Vx.
        Note: only sets a flag, does not actually block the
        emulator from executing other commands.
        :param vx:
        :return:
        """
        self.wait_for_keypress = True
        self.store_keypress_in_v = vx

    def ld_dt_v(self, vx: int) -> None:
        self.dt_register = self.v_registers[vx]

    def ld_st_v(self, vx: int) -> None:
        self.st_register = self.v_registers[vx]

    def add_i_v(self, vx: int) -> None:
        """
        Add I and Vx together and store the result in I. Since
        registers are only 8-bit, mod the result in range [0, 0xFF].
        :param vx: The "x" in Vx
        """
        self.i_register = (self.i_register + self.v_registers[vx]) % Emulator.MOD_8_BIT

    def ld_f_v(self, vx: int) -> None:
        self.i_register = self.v_registers[vx] * Emulator.FONT_SIZE

    def ld_b_v(self, vx: int) -> None:
        self.memory[self.i_register] = self.v_registers[vx] // 100
        self.memory[self.i_register + 1] = self.v_registers[vx] % 100 // 10
        self.memory[self.i_register + 2] = self.v_registers[vx] % 10

    def ld_i_v(self, vx: int) -> None:
        for i in range(0xF):
            self.memory[self.i_register + i] = self.v_registers[i]

    def ld_v_i(self, vx: int) -> None:
        for i in range(0xF):
            self.v_registers[i] = self.memory[self.i_register + i]

    def increment_program_counter(self, num_ops: int = 1) -> None:
        self.program_counter += num_ops * 2  # Each opcode is 2 bytes

    def key_down(self, keypress: str):
        try:
            code = int(keypress, 16)
            self.keys_pressed.append(code)

            if self.wait_for_keypress is True:
                self.v_registers[self.store_keypress_in_v] = code
                self.wait_for_keypress = False
                self.store_keypress_in_v = None
        except ValueError:
            pass

    def key_up(self, keypress: str):
        try:
            code = int(keypress, 16)
            self.keys_pressed.remove(code)
        except ValueError:
            pass

    def __str__(self):
        value = '-' * 66 + '\n'
        for row in self.display:
            value += '|'
            for col in row:
                value += '.' if col else ' '
            value += '|\n'
        value += '-' * 66
        return value

    @staticmethod
    def empty_display() -> list:
        display = []
        for row in range(32):
            display.append([False] * 64)
        return display

    @staticmethod
    def _init_fonts(memory: bytearray):
        i = 0
        for font in Emulator.FONTS:
            for row in font:
                memory[i] = row
                i += 1

    @staticmethod
    def _read_source(source: IO[bytes], dest: bytearray, start: int) -> int:
        byte = source.read(1)
        while byte:
            dest[start] = int.from_bytes(byte, 'big')
            start += 1
            byte = source.read(1)
        return start
