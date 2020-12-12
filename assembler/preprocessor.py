import re
import sys
from typing import List


class Preprocessor:
    PROGRAM_START = 0x200
    OPCODE_SIZE = 2

    def __init__(self):
        self.labels = {}
        self.defines = {}
        self.processed_lines = []
        self.program_counter = Preprocessor.PROGRAM_START

    @staticmethod
    def remove_comment(line: str) -> tuple:
        return line.split(';', 1)[0].strip()

    @staticmethod
    def split_label(line: str) -> tuple:
        """
        Given a line of assembly, split apart the label and the instruction.
        Only one label may exist on a single line. To declare two labels,
        put them on separate lines.
        :param line: Line of ASM code that may or may not contain a label.
        :return: (Label, Instruction), either may be None
        """
        label, colon, instruction = [None if s == '' else s.strip() for s in line.partition(':')]
        if colon:
            if re.match(r'^[a-zA-Z_][0-9a-zA-Z_]*$', label):
                return label, instruction
            else:
                raise ValueError('Invalid label: ' + line)
        else:
            return None, label  # label is set to the entire instruction

    @staticmethod
    def get_define(line: str) -> tuple:
        """
        Given a line of code, determine if it is a define. If so, split
        it into the label and value.
        :param source: ASM code to parse
        :return: (label, value) if applicable, else None
        """
        if line and line.startswith('define'):
            m = re.match(r'^define\s+([a-zA-Z][a-zA-Z0-9_]*)\s+([a-zA-Z0-9_]*)$', line)
            if m is None:
                raise ValueError('Invalid define: ' + line)
            else:
                return m.group(1), m.group(2)
        else:
            return None

    @staticmethod
    def split_mnemonic(line: str) -> tuple:
        """
        Split the line into mnemonic and list of operands. If line is empty, returns (None, []).
        """
        split = line.split(maxsplit=1)
        if split:
            mnemonic, operands = split[0], split[1:]
            if operands:
                operands = re.split(r',\s*', operands[0])
            return mnemonic, operands
        else:
            return None, []

    def register_label(self, key: str) -> None:
        if key in self.labels:
            raise ValueError('Multiple declarations of label: ' + key)
        else:
            self.labels[key] = '0x' + hex(self.program_counter)[2:].zfill(3)

    def register_define(self, key: str, value: str) -> None:
        if key in self.labels:
            raise ValueError('Multiple declarations of definition: ' + key)
        else:
            self.labels[key] = value

    def first_pass(self, source: List[str]) -> None:
        """
        Remove comments, build labels and defines.
        :param source:
        :return:
        """
        for line_num, line in enumerate(source):
            line = Preprocessor.remove_comment(line)
            label, line = Preprocessor.split_label(line)
            define = Preprocessor.get_define(line)
            if label is not None:
                self.register_label(label)
            if define is not None:
                self.register_define(*define)
                line = ''
            if line:
                self.program_counter += 2
                self.processed_lines.append(line)

    def second_pass(self) -> None:
        """
        Format each line. Replace labels and defines with their respective values.
        :return:
        """
        for line_num, line in enumerate(self.processed_lines):
            mnemonic, operands = self.split_mnemonic(line)
            if mnemonic:
                if operands:
                    for op_num, op in enumerate(operands):
                        operands[op_num] = self.labels.get(op, op)
                    self.processed_lines[line_num] = mnemonic + ' ' + ', '.join(operands)
                else:
                    self.processed_lines[line_num] = mnemonic

    def preprocess(self, source: list) -> list:
        self.first_pass(source)
        self.second_pass()
        return self.processed_lines


def main() -> None:
    """
    Preprocess the file at the given path and print the result
    """
    if len(sys.argv) != 2:
        print('Usage: $ python3 preprocessor.py <source>')
    else:
        with open(sys.argv[1], 'r') as source:
            for line in Preprocessor().preprocess(source.readlines()):
                print(line)


if __name__ == '__main__':
    main()