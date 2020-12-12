from io import BytesIO
from unittest import TestCase

from emulator import Emulator


class TestEmulator(TestCase):

    def test_add_i_v(self) -> None:
        emulator = Emulator(source=None)
        emulator.i_register = 0xF0
        emulator.v_registers[0] = 0xC
        emulator.v_registers[1] = 0x3
        emulator.v_registers[2] = 0xA

        # Standard addition
        emulator.add_i_v(0)
        self.assertEqual(0xFC, emulator.i_register)

        # Add to max
        emulator.add_i_v(1)
        self.assertEqual(0xFF, emulator.i_register)

        # 8-bit overflow
        emulator.add_i_v(2)
        self.assertEqual(0x9, emulator.i_register)

    def test_add_v_byte(self) -> None:
        emulator = Emulator(source=None)
        emulator.v_registers[0] = 0xF0

        # Standard addition
        emulator.add_v_byte(0, 0xC)
        self.assertEqual(0xFC, emulator.v_registers[0])

        # Add to max
        emulator.add_v_byte(0, 0x3)
        self.assertEqual(0xFF, emulator.v_registers[0])

        # 8-bit overflow
        emulator.add_v_byte(0, 0xA)
        self.assertEqual(0x9, emulator.v_registers[0])

    def test_add_v_v(self) -> None:
        emulator = Emulator(source=None)
        emulator.v_registers[0] = 0xF0
        emulator.v_registers[1] = 0xC
        emulator.v_registers[2] = 0xA

        # Standard addition
        emulator.add_v_v(0, 1)
        self.assertEqual(0xFC, emulator.v_registers[0])

        # 8-bit overflow
        emulator.add_v_v(0, 2)
        self.assertEqual(0x6, emulator.v_registers[0])

    def test_jp_address(self):
        emulator = Emulator(source=None)
        emulator.program_counter = 0x500

        emulator.jp_address(0x700)
        self.assertEqual(0x700, emulator.program_counter)

        emulator.jp_address(0xFFF)
        self.assertEqual(0xFFF, emulator.program_counter)

    def test_or_v_v(self):
        emulator = Emulator(source=None)
        emulator.v_registers[0] = 0xA5  # 10100101
        emulator.v_registers[1] = 0x12  # 00010010

        emulator.or_v_v(0, 1)
        self.assertEqual(0xB7, emulator.v_registers[0])

    def test_shl_v(self):
        emulator = Emulator(source=None)
        emulator.v_registers[0] = 0xA5  # 10100101

        emulator.shl_v(0)
        self.assertEqual(1, emulator.v_registers[0xF])
        self.assertEqual(0x4A, emulator.v_registers[0])

        emulator.shl_v(0)
        self.assertEqual(0, emulator.v_registers[0xF])
        self.assertEqual(0x94, emulator.v_registers[0])

    def test_skp_v(self):
        emulator = Emulator(source=None)
        emulator.v_registers[3] = 0xC

        self.assertFalse(emulator.skp_v(3))

        emulator.key_down('C')
        self.assertTrue(emulator.skp_v(3))

        emulator.key_up('C')
        self.assertFalse(emulator.skp_v(3))
