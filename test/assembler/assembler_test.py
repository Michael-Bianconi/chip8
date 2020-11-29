from unittest import TestCase

from assembler.assembler import assemble

class AssemblerTest(TestCase):

    def test_assemble_add_i_v(self):
        self.assertEqual(0xF41E, assemble("ADD I, V4"))
        self.assertEqual(0xF41E, assemble("adD I, V04"))
        self.assertEqual(0xF41E, assemble("ADD    I, V4"))
        self.assertEqual(0xF41E, assemble("ADD I   , V4"))
        self.assertEqual(0xF41E, assemble("ADD I,    V4"))
        self.assertEqual(0xF41E, assemble("ADD i, v0004"))
        self.assertEqual(0xF01E, assemble("ADD I, V0"))
        self.assertEqual(0xFF1E, assemble("ADD I, VF"))
        self.assertIsNone(assemble("ADD I, F"))
        self.assertIsNone(assemble("ADD I  V6"))
        self.assertIsNone(assemble("ADD I, Vx"))
        self.assertIsNone(assemble("ADD I, V-4"))

    def test_assemble_add_v_b(self):
        self.assertEqual(0x7405, assemble("ADD V4, 5"))
        self.assertEqual(0x7405, assemble("adD V4, 05"))
        self.assertEqual(0x7405, assemble("ADD    V4, 5"))
        self.assertEqual(0x7405, assemble("ADD     V4, 005"))
        self.assertEqual(0x7405, assemble("ADD v4, 5"))
        self.assertEqual(0x70f6, assemble("ADD V0, 0xf6"))
        self.assertEqual(0x701a, assemble("ADD V0, 1a"))
        self.assertIsNone(assemble("add V4"))
        self.assertIsNone(assemble("ADD Vg, 0xf5"))
        self.assertIsNone(assemble("ADD Va, -0xf"))
        self.assertIsNone(assemble("ADD V4, 0xx"))
        self.assertIsNone(assemble("ADD V4, 0xffa"))
        self.assertIsNone(assemble("ADD V0x4, 0xffa"))

    def test_assemble_add_v_v(self):
        self.assertEqual(0x8454, assemble("ADD V4, V5"))
        self.assertEqual(0x8454, assemble("adD V4, V05"))
        self.assertEqual(0x8454, assemble("ADD    V4, V5"))
        self.assertEqual(0x8454, assemble("ADD  V4, V00005"))
        self.assertEqual(0x8454, assemble("ADD     V4, V005"))
        self.assertEqual(0x8454, assemble("ADD v4, V5"))
        self.assertEqual(0x80F4, assemble("ADD V0, Vf"))
        self.assertEqual(0x8A14, assemble("ADD Va, V1"))
        self.assertIsNone(assemble("ADD Vg, V0xf5"))
        self.assertIsNone(assemble("ADD Va, -0xf"))
        self.assertIsNone(assemble("ADD V4, 0xx"))
        self.assertIsNone(assemble("ADD V4, 0xffa"))
        self.assertIsNone(assemble("ADD 4, V6"))
