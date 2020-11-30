from unittest import TestCase
from disassembler import mnemonic


class DisassemblerTest(TestCase):

    def test_mnemonic_jp(self):
        self.assertEqual('JP 0x000', mnemonic('1000'))
        self.assertEqual('JP 0xFFF', mnemonic('1FFF'))

    def test_mnemonic_se(self):
        self.assertEqual('SE V0, 0x05', mnemonic('3005'))
        self.assertEqual('SE V1, 0xFF', mnemonic('31FF'))