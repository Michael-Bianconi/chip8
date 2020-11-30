import filecmp
from unittest import TestCase
import tempfile, os

from assembler import assemble_file
from disassembler import disassemble


class AssembleDisassembleTest(TestCase):
    """
    The assemble-disassemble test asserts that a round-trip of
    assembly-disassembly will result in the same code. However,
    since the preprocessor alters the code prior to assembly,
    we cannot simply compare the original source file and the
    disassembled source file. Instead, we reassemble the disassembled
    source and compare the binary files. Those binary files should be
    guaranteed to be identical.
    """

    def assertAssembled(self, src_path: str) -> None:
        """
        Assemble source code into binary, disassemble it
        back into source code, then assemble it into binary again.
        Compare the two binary files. If they are identical,
        then both the assembler and disassembler work as intended
        for that given source code.

        Do not pass code with errors in it.
        :param src_path:
        :return:
        """
        dest1_fd, dest1_path = tempfile.mkstemp()
        src2_fd, src2_path = tempfile.mkstemp(text=True)
        dest2_fd, dest2_path = tempfile.mkstemp()

        # Assemble
        with open(src_path, 'r') as src:
            with open(dest1_path, 'wb') as dest:
                assemble_file(src, dest)

        # Disassemble
        with open(dest1_path, 'rb') as src:
            with open(src2_path, 'w') as dest:
                dest.write('\n'.join([line for line in disassemble(src) if line]))

        # Assemble again
        with open(src2_path, 'r') as src:
            with open(dest2_path, 'wb') as dest:
                assemble_file(src, dest)

        # Sanity check
        self.assertNotEqual(0, os.stat(dest1_path).st_size)

        # Compare binary files
        if not filecmp.cmp(dest1_path, dest2_path):
            with open(src_path, 'r') as expected_src:
                with open(src2_path, 'r') as actual_src:
                    print('Original source:')
                    print(expected_src.read())
                    print('\nReassembled:')
                    print(actual_src.read())
            self.fail()

        os.remove(src2_path)
        os.remove(dest1_path)
        os.remove(dest2_path)


    def test_all_source_samples(self):
        sources = 'samples/sources'
        for filename in os.listdir('samples/sources'):
            self.assertAssembled(os.path.join(sources, filename))