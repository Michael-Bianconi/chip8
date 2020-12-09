from unittest import TestCase
from disassembler import mnemonic


class DisassemblerTest(TestCase):

    def test_mnemonic_add(self):
        self.assertEqual('ADD V0, 0x56', mnemonic(0x7056))

    def test_mnemonic_jp(self):
        self.assertEqual('JP 0x000', mnemonic(0x1000))
        self.assertEqual('JP 0xFFF', mnemonic(0x1FFF))

    def test_mnemonic_ld(self):
        self.assertEqual('LD V0, 0x05', mnemonic(0x6005))
        self.assertEqual('LD V4, 0xFF', mnemonic(0x64FF))
        self.assertEqual('LD [I], V4', mnemonic(0xF455))

    def test_mnemonic_se(self):
        self.assertEqual('SE V0, 0x05', mnemonic(0x3005))
        self.assertEqual('SE V1, 0xFF', mnemonic(0x31FF))

    def test_mnemonic_sne(self):
        self.assertEqual('SNE V4, 0x43', mnemonic(0x4443))
