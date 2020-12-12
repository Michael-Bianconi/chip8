from unittest import TestCase

from assembler.operandtype import OperandType


class TestOperandType(TestCase):

    def test_parse_v(self):
        self.assertEquals(0, OperandType.parse(OperandType.V, 'V0'))
        self.assertEquals(5, OperandType.parse(OperandType.V, 'v5'))
        self.assertEquals(0xF, OperandType.parse(OperandType.V, 'vf'))
        self.assertEquals(0xF, OperandType.parse(OperandType.V, 'vF'))
        self.assertIsNone(OperandType.parse(OperandType.V, 'g0'))
        self.assertIsNone(OperandType.parse(OperandType.V, 'vH'))
        self.assertIsNone(OperandType.parse(OperandType.V, 'v    f'))
        self.assertIsNone(OperandType.parse(OperandType.V, ''))
        self.assertIsNone(OperandType.parse(OperandType.V, 'v0v1'))

    def test_parse_ai(self):
        self.assertEquals('[I]', OperandType.parse(OperandType.AI, '[I]'))
        self.assertEquals('[I]', OperandType.parse(OperandType.AI, '[i]'))
        self.assertIsNone(OperandType.parse(OperandType.AI, 'I'))
        self.assertIsNone(OperandType.parse(OperandType.AI, 'I]'))
        self.assertIsNone(OperandType.parse(OperandType.AI, '[I'))

    def test_parse_nibble(self):
        for i in range(0x10):
            self.assertEquals(i, OperandType.parse(OperandType.NIBBLE, str(i)))
            self.assertEquals(i, OperandType.parse(OperandType.NIBBLE, str(i).zfill(2)))
            self.assertEquals(i, OperandType.parse(OperandType.NIBBLE, str(i).zfill(3)))
            self.assertEquals(i, OperandType.parse(OperandType.NIBBLE, str(i).zfill(10)))

            self.assertEquals(i, OperandType.parse(OperandType.NIBBLE, hex(i)))
            self.assertEquals(i, OperandType.parse(OperandType.NIBBLE, '0x' + hex(i)[2:].zfill(2)))
            self.assertEquals(i, OperandType.parse(OperandType.NIBBLE, '0x' + hex(i)[2:].zfill(3)))
            self.assertEquals(i, OperandType.parse(OperandType.NIBBLE, '0x' + hex(i)[2:].zfill(10)))

            self.assertEquals(i, OperandType.parse(OperandType.NIBBLE, '#' + hex(i)))
            self.assertEquals(i, OperandType.parse(OperandType.NIBBLE, '#' + hex(i)[2:].zfill(2)))
            self.assertEquals(i, OperandType.parse(OperandType.NIBBLE, '#' + hex(i)[2:].zfill(3)))
            self.assertEquals(i, OperandType.parse(OperandType.NIBBLE, '#' + hex(i)[2:].zfill(10)))
        self.assertIsNone(OperandType.parse(OperandType.NIBBLE, 'V0'))
        self.assertIsNone(OperandType.parse(OperandType.NIBBLE, 'F'))
        with self.assertRaises(ValueError): OperandType.parse(OperandType.NIBBLE, '0xFF')

    def test_parse_byte(self):
        for i in range(0x100):
            self.assertEquals(i, OperandType.parse(OperandType.BYTE, str(i)))
            self.assertEquals(i, OperandType.parse(OperandType.BYTE, str(i).zfill(2)))
            self.assertEquals(i, OperandType.parse(OperandType.BYTE, str(i).zfill(3)))
            self.assertEquals(i, OperandType.parse(OperandType.BYTE, str(i).zfill(10)))

            self.assertEquals(i, OperandType.parse(OperandType.BYTE, hex(i)))
            self.assertEquals(i, OperandType.parse(OperandType.BYTE, '0x' + hex(i)[2:].zfill(2)))
            self.assertEquals(i, OperandType.parse(OperandType.BYTE, '0x' + hex(i)[2:].zfill(3)))
            self.assertEquals(i, OperandType.parse(OperandType.BYTE, '0x' + hex(i)[2:].zfill(10)))

            self.assertEquals(i, OperandType.parse(OperandType.BYTE, '#' + hex(i)))
            self.assertEquals(i, OperandType.parse(OperandType.BYTE, '#' + hex(i)[2:].zfill(2)))
            self.assertEquals(i, OperandType.parse(OperandType.BYTE, '#' + hex(i)[2:].zfill(3)))
            self.assertEquals(i, OperandType.parse(OperandType.BYTE, '#' + hex(i)[2:].zfill(10)))
        self.assertIsNone(OperandType.parse(OperandType.BYTE, 'F'))
        with self.assertRaises(ValueError): OperandType.parse(OperandType.BYTE, '0xFFF')

    def test_parse_addr(self):

        for i in range(0x1000):
            self.assertEquals(i, OperandType.parse(OperandType.ADDR, str(i)))
            self.assertEquals(i, OperandType.parse(OperandType.ADDR, str(i).zfill(2)))
            self.assertEquals(i, OperandType.parse(OperandType.ADDR, str(i).zfill(3)))
            self.assertEquals(i, OperandType.parse(OperandType.ADDR, str(i).zfill(10)))

            self.assertEquals(i, OperandType.parse(OperandType.ADDR, hex(i)))
            self.assertEquals(i, OperandType.parse(OperandType.ADDR, '0x' + hex(i)[2:].zfill(2)))
            self.assertEquals(i, OperandType.parse(OperandType.ADDR, '0x' + hex(i)[2:].zfill(3)))
            self.assertEquals(i, OperandType.parse(OperandType.ADDR, '0x' + hex(i)[2:].zfill(10)))

            self.assertEquals(i, OperandType.parse(OperandType.ADDR, '#' + hex(i)))
            self.assertEquals(i, OperandType.parse(OperandType.ADDR, '#' + hex(i)[2:].zfill(2)))
            self.assertEquals(i, OperandType.parse(OperandType.ADDR, '#' + hex(i)[2:].zfill(3)))
            self.assertEquals(i, OperandType.parse(OperandType.ADDR, '#' + hex(i)[2:].zfill(10)))
