import sys
from typing import TextIO, IO

from assembler.operandtype import OperandType
from assembler.preprocessor import Preprocessor


class Assembler:

    _INSTRUCTION_FORMATS = {
        'ADD': (
            {'format': [OperandType.I, OperandType.V],
             'assemble': lambda args: 0xF01E | (args[2] << 8)},
            {'format': [OperandType.V, OperandType.BYTE],
             'assemble': lambda args: 0x7000 | (args[1] << 8) | (args[2])},
            {'format': [OperandType.V, OperandType.V],
             'assemble': lambda args: 0x8004 | (args[1] << 8) | (args[2] << 4)},),
        'AND': (
            {'format': [OperandType.V, OperandType.V],
             'assemble': lambda args: 0x8002 | (args[1] << 8) | (args[2] << 4)},),
        'CALL': (
            {'format':[OperandType.ADDR],
             'assemble': lambda args: 0x2000 | args[1]},),
        'CLS': (
            {'format': [],
             'assemble': lambda args: 0x00E0},),
        'DRW': (
            {'format': [OperandType.V, OperandType.V, OperandType.NIBBLE],
             'assemble': lambda args: 0xD000 | (args[1] << 8) | (args[2] << 4) | args[3]},),
        'JP': (
            {'format': [OperandType.ADDR],
             'assemble': lambda args: 0x1000 | args[1]},
            {'format': [OperandType.V0, OperandType.ADDR],
             'assemble': lambda args: 0xB000 | args[2]},),
        'LD': (
            {'format': [OperandType.B, OperandType.V],
             'assemble': lambda args: 0xF033 | (args[2] << 8)},
            {'format': [OperandType.DT, OperandType.V],
             'assemble': lambda args: 0xF015 | (args[2] << 8)},
            {'format': [OperandType.F, OperandType.V],
             'assemble': lambda args: 0xF029 | (args[2] << 8)},
            {'format': [OperandType.I, OperandType.ADDR],
             'assemble': lambda args: 0xA000 | args[2]},
            {'format': [OperandType.AI, OperandType.V],
             'assemble': lambda args: 0xF055 | (args[2] << 8)},
            {'format': [OperandType.ST, OperandType.V],
             'assemble': lambda args: 0xF018 | (args[2] << 8)},
            {'format': [OperandType.V, OperandType.BYTE],
             'assemble': lambda args: 0x6000 | (args[1] << 8) | args[2]},
            {'format': [OperandType.V, OperandType.DT],
             'assemble': lambda args: 0xF007 | (args[1] << 8)},
            {'format': [OperandType.V, OperandType.AI],
             'assemble': lambda args: 0xF065 | (args[1] << 8)},
            {'format': [OperandType.V, OperandType.K],
             'assemble': lambda args: 0xF00A | (args[1] << 8)},
            {'format': [OperandType.V, OperandType.V],
             'assemble': lambda args: 0x8000 | (args[1] << 8) | (args[2] << 4)},),
        'OR': (
            {'format': [OperandType.V, OperandType.V],
             'assemble': lambda args: 0x8001 | (args[1] << 8) | (args[2] << 4)},),
        'RET': (
            {'format': [],
             'assemble': lambda args: 0x00EE},),
        'RND': (
            {'format': [OperandType.V, OperandType.BYTE],
             'assemble': lambda args: 0xC000 | (args[1] << 8) | args[2]},),
        'SE': (
            {'format': [OperandType.V, OperandType.BYTE],
             'assemble': lambda args: 0x3000 | (args[1] << 8) | args[2]},
            {'format': [OperandType.V, OperandType.V],
             'assemble': lambda args: 0x5000 | (args[1] << 8) | (args[2] << 4)},),
        'SHL': (
            {'format': [OperandType.V],
             'assemble': lambda args: 0x800E | (args[1] << 8)},
            {'format': [OperandType.V, OperandType.V],
             'assemble': lambda args: 0x800E | (args[1] << 8) | args[2] << 4}),
        'SHR': (
            {'format': [OperandType.V],
             'assemble': lambda args: 0x8006 | (args[1] << 8)},
            {'format': [OperandType.V, OperandType.V],
             'assemble': lambda args: 0x8006 | (args[1] << 8) | args[2] << 4}),
        'SKNP': (
            {'format': [OperandType.V],
             'assemble': lambda args: 0xE0A1 | (args[1] << 8)},),
        'SKP': (
            {'format': [OperandType.V],
             'assemble': lambda args: 0xE09E | (args[1] << 8)},),
        'SNE': (
            {'format': [OperandType.V, OperandType.BYTE],
             'assemble': lambda args: 0x4000 | (args[1] << 8) | args[2]},
            {'format': [OperandType.V, OperandType.V],
             'assemble': lambda args: 0x9000 | (args[1] << 8) | (args[2] << 4)},),
        'SUB': (
            {'format': [OperandType.V, OperandType.V],
             'assemble': lambda args: 0x8005 | (args[1] << 8) | (args[2] << 4)},),
        'SUBN': (
            {'format': [OperandType.V, OperandType.V],
             'assemble': lambda args: 0x8007 | (args[1] << 8) | (args[2] << 4)},),
        'SYS': (
            {'format': [OperandType.ADDR],
             'assemble': lambda args: args[1]},),
        'XOR': (
            {'format': [OperandType.V, OperandType.V],
             'assemble': lambda args: 0x8003 | (args[1] << 8) | (args[2] << 4)},),
    }

    @staticmethod
    def _get_formats(opcode: str) -> dict:
        opcode = opcode.upper().strip()
        if opcode not in Assembler._INSTRUCTION_FORMATS:
            raise ValueError('Unrecognized opcode: ' + opcode)
        else:
            return Assembler._INSTRUCTION_FORMATS[opcode]

    @staticmethod
    def _parse_line(line: str, *expected_operands: OperandType) -> list:
        return_val = []
        opcode, _, operands = line.upper().partition(' ')
        operands = [a for a in operands.split(',') if a]

        if len(operands) == len(expected_operands):
            return_val.append(opcode)
            for expected in expected_operands:
                actual = operands.pop(0).strip()
                match = OperandType.parse(expected, actual)
                if match is not None:
                    return_val.append(match)
                else:
                    return_val = None
                    break
        else:
            return_val = None

        return return_val

    @staticmethod
    def assemble_line(line: str) -> int:
        """
        Assembles a *processed* line of Chip-8 assembly. Processed
        lines should not include any pseudo-instructions, labels,
        or defines.
        :param line:
        :return:
        """
        opcode = line.split(' ', 1)[0]
        formats = Assembler._get_formats(opcode)
        for format in formats:
            args = Assembler._parse_line(line, *format['format'])
            if args is not None:
                return format['assemble'](args)
        return None

    @staticmethod
    def assemble_file(source: TextIO, dest: IO[bytes]) -> None:
        lines = Preprocessor().preprocess(source.readlines())
        data = []

        for line_num, line in enumerate(lines):
            opcode = None
            try:
                opcode = Assembler.assemble_line(line)
            except ValueError as e:
                print(f'Line {line_num}: {e}')
            if opcode is None:
                raise ValueError('Unrecognized line:' + line)
            data.append((opcode & 0xFF00) >> 8)
            data.append(opcode & 0xFF)

        dest.write(bytearray(data))


def main(argv: list) -> None:
    if len(argv) != 3:
        print('Usage: $ python3 assembler.py <source> <destination>')
        sys.exit(0)
    else:
        _, source_path, dest_path = argv
        with open(source_path, 'r') as source:
            with open(dest_path, 'wb+') as dest:
                Assembler.assemble_file(source, dest)


if __name__ == '__main__':
    main(sys.argv)