import enum, re, sys
from typing import TextIO, List, IO


class ArgType(enum.Enum):
    V = re.compile('^v0*([0-9a-f])$', re.IGNORECASE)
    V0 = re.compile('^(V0)$', re.IGNORECASE)
    B = re.compile('^(B)$', re.IGNORECASE)
    F = re.compile('^(F)$', re.IGNORECASE)
    DT = re.compile('^(DT)$', re.IGNORECASE)
    ST = re.compile('^(ST)$', re.IGNORECASE)
    I = re.compile('^(I)$', re.IGNORECASE)
    K = re.compile('^(K)$', re.IGNORECASE)
    AI = re.compile('^(\\[I])$', re.IGNORECASE)
    NIBBLE = re.compile('^(?:0x|#)0*([0-9a-f])$', re.IGNORECASE)
    BYTE = re.compile('^(?:0x|#)0*([0-9a-f]|[0-9a-f]{2})$', re.IGNORECASE)
    ADDR = re.compile('^(?:0x|#)0*([0-9a-f]|[0-9a-f]{2}|[0-9a-f]{3})$', re.IGNORECASE)


def get_formats(opcode: str) -> dict:
    formats = {
        'ADD': (
            {'format': [ArgType.I, ArgType.V],
             'assemble': lambda args: 0xF01E | (args[2] << 8)},
            {'format': [ArgType.V, ArgType.BYTE],
             'assemble': lambda args: 0x7000 | (args[1] << 8) | (args[2])},
            {'format': [ArgType.V, ArgType.V],
             'assemble': lambda args: 0x8004 | (args[1] << 8) | (args[2] << 4)},),
        'AND': (
            {'format': [ArgType.V, ArgType.V],
             'assemble': lambda args: 0x8002 | (args[1] << 8) | (args[2] << 4)},),
        'CALL': (
            {'format':[ArgType.ADDR],
             'assemble': lambda args: 0x2000 | args[1]},),
        'CLS': (
            {'format': [],
             'assemble': lambda args: 0x00E0},),
        'DRW': (
            {'format': [ArgType.V, ArgType.V, ArgType.NIBBLE],
             'assemble': lambda args: 0xD000 | (args[1] << 8) | (args[2] << 4) | args[3]},),
        'JP': (
            {'format': [ArgType.ADDR],
             'assemble': lambda args: 0x1000 | args[1]},
            {'format': [ArgType.V0, ArgType.ADDR],
             'assemble': lambda args: 0xB000 | args[2]},),
        'LD': (
            {'format': [ArgType.B, ArgType.V],
             'assemble': lambda args: 0xF033 | (args[2] << 8)},
            {'format': [ArgType.DT, ArgType.V],
             'assemble': lambda args: 0xF015 | (args[2] << 8)},
            {'format': [ArgType.F, ArgType.V],
             'assemble': lambda args: 0xF029 | (args[2] << 8)},
            {'format': [ArgType.I, ArgType.ADDR],
             'assemble': lambda args: 0xA000 | args[2]},
            {'format': [ArgType.AI, ArgType.V],
             'assemble': lambda args: 0xF055 | (args[2] << 8)},
            {'format': [ArgType.ST, ArgType.V],
             'assemble': lambda args: 0xF018 | (args[2] << 8)},
            {'format': [ArgType.V, ArgType.BYTE],
             'assemble': lambda args: 0x6000 | (args[1] << 8) | args[2]},
            {'format': [ArgType.V, ArgType.DT],
             'assemble': lambda args: 0xF007 | (args[1] << 8)},
            {'format': [ArgType.V, ArgType.AI],
             'assemble': lambda args: 0xF065 | (args[1] << 8)},
            {'format': [ArgType.V, ArgType.K],
             'assemble': lambda args: 0xF00A | (args[1] << 8)},
            {'format': [ArgType.V, ArgType.V],
             'assemble': lambda args: 0x8000 | (args[1] << 8) | (args[2] << 4)},),
        'OR': (
            {'format': [ArgType.V, ArgType.V],
             'assemble': lambda args: 0x8001 | (args[1] << 8) | (args[2] << 4)},),
        'RET': (
            {'format': [],
             'assemble': lambda args: 0x00EE},),
        'RND': (
            {'format': [ArgType.V, ArgType.BYTE],
             'assemble': lambda args: 0xC000 | (args[1] << 8) | args[2]},),
        'SE': (
            {'format': [ArgType.V, ArgType.BYTE],
             'assemble': lambda args: 0x3000 | (args[1] << 8) | args[2]},
            {'format': [ArgType.V, ArgType.V],
             'assemble': lambda args: 0x5000 | (args[1] << 8) | (args[2] << 4)},),
        'SHL': (
            {'format': [ArgType.V],
             'assemble': lambda args: 0x800E | (args[1] << 8)},
            {'format': [ArgType.V, ArgType.V],
             'assemble': lambda args: 0x800E | (args[1] << 8) | args[2] << 4}),
        'SHR': (
            {'format': [ArgType.V],
             'assemble': lambda args: 0x8006 | (args[1] << 8)},
            {'format': [ArgType.V, ArgType.V],
             'assemble': lambda args: 0x8006 | (args[1] << 8) | args[2] << 4}),
        'SKNP': (
            {'format': [ArgType.V],
             'assemble': lambda args: 0xE0A1 | (args[1] << 8)},),
        'SKP': (
            {'format': [ArgType.V],
             'assemble': lambda args: 0xE09E | (args[1] << 8)},),
        'SNE': (
            {'format': [ArgType.V, ArgType.BYTE],
             'assemble': lambda args: 0x4000 | (args[1] << 8) | args[2]},
            {'format': [ArgType.V, ArgType.V],
             'assemble': lambda args: 0x9000 | (args[1] << 8) | (args[2] << 4)},),
        'SUB': (
            {'format': [ArgType.V, ArgType.V],
             'assemble': lambda args: 0x8005 | (args[1] << 8) | (args[2] << 4)},),
        'SUBN': (
            {'format': [ArgType.V, ArgType.V],
             'assemble': lambda args: 0x8007 | (args[1] << 8) | (args[2] << 4)},),
        'SYS': (
            {'format': [ArgType.ADDR],
             'assemble': lambda args: args[1]},),
        'XOR': (
            {'format': [ArgType.V, ArgType.V],
             'assemble': lambda args: 0x8003 | (args[1] << 8) | (args[2] << 4)},),
    }
    if opcode.upper().strip() not in formats:
        raise ValueError('Unrecognized opcode: ' + opcode)
    else:
        return formats[opcode.upper().strip()]


def parseMnemonic(line: str, *expected_args: ArgType) -> list:
    retval = []
    opcode, _, args = line.partition(' ')
    args = [a for a in args.split(',') if a]

    if len(args) != len(expected_args):
        retval = None
    else:
        retval.append(opcode)

        for expected_arg in expected_args:
            arg = args.pop(0).strip()
            match = expected_arg.value.match(arg)
            if match is not None:
                try:
                    retval.append(int(match.group(1), 16))
                except ValueError:
                    retval.append(match.group(1))
            else:
                retval = None
                break

    return retval


def split_label(source: str) -> tuple:
    label, colon, instruction = source.partition(':')
    if label and colon:
        if label[0].isalpha() and label.isalnum():
            return label.strip(), instruction.strip()
        else:
            raise ValueError('Invalid label: ' + source)
    else:
        return None, source


def get_define(source: str) -> tuple:
    m = re.match('^define ([a-zA-Z][a-zA-Z0-9_]*)\s+([a-zA-Z0-9_]*)$', source)
    if m is None:
        return None
    else:
        return m.group(1), m.group(2)


def preprocess(source: List[str]) -> list:
    program_counter = 0
    labels = {}
    destination = []
    for line_num, line in enumerate(source):
        line = line.split(';', 1)[0].strip()
        label, line = split_label(line)
        define = get_define(line)
        if label is not None:
            labels[label] = f'0x{program_counter:03}'
        if define is not None:
            labels[define[0]] = define[1]
            line = ''
        if line:
            program_counter += 1
            destination.append(line)
    for line_num, line in enumerate(destination):
        split = line.split(maxsplit=1)
        mnemonic, operands = split[0], split[1:]
        if operands:
            operands = re.split(',\s*', operands[0])
            for op_num, op in enumerate(operands):
                operands[op_num] = labels.get(op, op)
            destination[line_num] = mnemonic + ' ' + ', '.join(operands)
        else:
            destination[line_num] = mnemonic
    return destination


def assemble(line: str) -> int:
    """
    Assembles a *processed* line of Chip-8 assembly. Processed
    lines should not include any pseudo-instructions, labels,
    or defines.
    :param line:
    :return:
    """
    opcode = line.split(' ', 1)[0]
    formats = get_formats(opcode)
    for format in formats:
        args = parseMnemonic(line, *format['format'])
        if args is not None:
            return format['assemble'](args)
    return None


def assemble_file(source: TextIO, dest: IO[bytes]) -> None:
    lines = preprocess(source.readlines())
    data = []

    for line in lines:
        opcode = assemble(line)
        if opcode is None:
            raise ValueError('Unrecognized line:' + line)
        data.append((opcode & 0xFF00) >> 8)
        data.append(opcode & 0xFF)

    dest.write(bytearray(data))


def main(argv: list) -> None:
    print(argv)
    if len(argv) != 3:
        print('Usage: $ python3 assembler.py <source> <destination>')
        sys.exit(0)
    else:
        _, source_path, dest_path = argv
        with open(source_path, 'r') as source:
            with open(dest_path, 'wb+') as dest:
                assemble_file(source, dest)


if __name__ == '__main__':
    main(sys.argv)