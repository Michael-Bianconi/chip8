from unittest import TestCase

from assembler.assembler import assemble

class AssemblerTest(TestCase):

    def assertAssembles(self, expected, line):
        self.assertEqual(expected, assemble(line))

    def assertNotAssembles(self, line):
        self.assertIsNone(assemble(line))

    def test_assemble_add_i_v(self):
        self.assertAssembles(0xF41E, "ADD I, V4")
        self.assertAssembles(0xF41E, "adD I, V04")
        self.assertAssembles(0xF41E, "ADD    I, V4")
        self.assertAssembles(0xF41E, "ADD I   , V4")
        self.assertAssembles(0xF41E, "ADD I,    V4")
        self.assertAssembles(0xF41E, "ADD i, v0004")
        self.assertAssembles(0xF01E, "ADD I, V0")
        self.assertAssembles(0xFF1E, "ADD I, VF")
        self.assertNotAssembles("ADD I, F")
        self.assertNotAssembles("ADD I  V6")
        self.assertNotAssembles("ADD I, Vx")
        self.assertNotAssembles("ADD I, V-4")

    def test_assemble_add_v_b(self):
        self.assertAssembles(0x7405, "ADD V4, 5")
        self.assertAssembles(0x7405, "adD V4, 05")
        self.assertAssembles(0x7405, "ADD    V4, 5")
        self.assertAssembles(0x7405, "ADD     V4, 005")
        self.assertAssembles(0x7405, "ADD v4, 5")
        self.assertAssembles(0x70f6, "ADD V0, 0xf6")
        self.assertAssembles(0x701a, "ADD V0, 1a")
        self.assertNotAssembles("add V4")
        self.assertNotAssembles("ADD Vg, 0xf5")
        self.assertNotAssembles("ADD Va, -0xf")
        self.assertNotAssembles("ADD V4, 0xx")
        self.assertNotAssembles("ADD V4, 0xffa")
        self.assertNotAssembles("ADD V0x4, 0xffa")

    def test_assemble_add_v_v(self):
        self.assertAssembles(0x8454, "ADD V4, V5")
        self.assertAssembles(0x8454, "adD V4, V05")
        self.assertAssembles(0x8454, "ADD    V4, V5")
        self.assertAssembles(0x8454, "ADD  V4, V00005")
        self.assertAssembles(0x8454, "ADD     V4, V005")
        self.assertAssembles(0x8454, "ADD v4, V5")
        self.assertAssembles(0x80F4, "ADD V0, Vf")
        self.assertAssembles(0x8A14, "ADD Va, V1")
        self.assertNotAssembles("ADD Vg, V0xf5")
        self.assertNotAssembles("ADD Va, -0xf")
        self.assertNotAssembles("ADD V4, 0xx")
        self.assertNotAssembles("ADD V4, 0xffa")
        self.assertNotAssembles("ADD 4, V6")

    def test_assemble_drw(self):
        self.assertAssembles(0xD123, "DRW V1, V2, 3")
        self.assertAssembles(0xD00F, "drw  v0 ,  v0 ,  0x00000F")
        self.assertNotAssembles("drw v5, 5, 0x0F")