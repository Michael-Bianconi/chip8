from unittest import TestCase

from assembler.preprocessor import Preprocessor


class TestPreprocessor(TestCase):

    def test_remove_comment(self):
        # Empty
        self.assertEqual('', Preprocessor.remove_comment(''))
        # No comment
        self.assertEqual('ADD V0, V1', Preprocessor.remove_comment('ADD V0, V1'))
        # Line-comment
        self.assertEqual('', Preprocessor.remove_comment('  ; My comment  '))
        # Inline comment
        self.assertEquals('ADD V0, V1', Preprocessor.remove_comment('ADD V0, V1  ; My ; Comment'))

    def test_split_label(self):
        # Empty
        self.assertSequenceEqual((None, None), Preprocessor.split_label(''))
        # No label
        self.assertSequenceEqual((None, 'LD V0, 0x5'), Preprocessor.split_label('LD V0, 0x5'))
        # Label, no instruction
        self.assertSequenceEqual(('MyLabel', None), Preprocessor.split_label('MyLabel:'))
        # Label and instruction
        self.assertSequenceEqual(('MyLabel', 'ADD V0, 0x5'), Preprocessor.split_label('MyLabel: ADD V0, 0x5'))
        # Two labels
        self.assertSequenceEqual(('First', 'Second: SUB V0, V1'), Preprocessor.split_label('First: Second: SUB V0, V1'))
        # Invalid label
        with self.assertRaises(ValueError): Preprocessor.split_label('1label:')
        with self.assertRaises(ValueError): Preprocessor.split_label('label&:')
        with self.assertRaises(ValueError): Preprocessor.split_label('my label:')

    def test_split_mnemonic(self):
        # Empty
        self.assertSequenceEqual((None, []), Preprocessor.split_mnemonic(''))
        # No operands
        self.assertSequenceEqual(('ADD', []), Preprocessor.split_mnemonic('ADD'))
        # One operand
        self.assertSequenceEqual(('ADD', ['V0']), Preprocessor.split_mnemonic('ADD V0'))
        # Two operands
        self.assertSequenceEqual(('ADD', ['V0', 'V1']), Preprocessor.split_mnemonic('ADD V0, V1'))
        # Three operands
        self.assertSequenceEqual(('ADD', ['V0', 'V1', 'V2']), Preprocessor.split_mnemonic('ADD V0, V1, V2'))

    def test_get_define(self):
        # Empty
        self.assertIsNone(Preprocessor.get_define(''))
        # No define
        self.assertIsNone(Preprocessor.get_define('ADD V0, V1'))
        # Define
        self.assertSequenceEqual(('MyDefine', '1'), Preprocessor.get_define('define MyDefine 1'))
        # Invalid define
        with self.assertRaises(ValueError): Preprocessor.get_define('define 3define 1')
        with self.assertRaises(ValueError): Preprocessor.get_define('define my define 1')
        with self.assertRaises(ValueError): Preprocessor.get_define('define my&define 1')