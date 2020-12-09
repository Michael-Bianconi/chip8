import string
import sys
from typing import IO, TextIO

_patterns = {
    (0x00E0, 0xFFFF): lambda op: 'CLS',
    (0x00EE, 0xFFFF): lambda op: 'RET',
    (0x0000, 0xF000): lambda op: 'SYS 0x' + op[1:],
    (0x1000, 0xF000): lambda op: 'JP 0x' + op[1:],
    (0x2000, 0xF000): lambda op: 'CALL 0x' + op[1:],
    (0x3000, 0xF000): lambda op: 'SE V' + op[1] + ', 0x' + op[2:],
    (0x4000, 0xF000): lambda op: 'SNE V' + op[1] + ', 0x' + op[2:],
    (0x5000, 0xF00F): lambda op: 'SE V' + op[1] + ', V' + op[2],
    (0x6000, 0xF000): lambda op: 'LD V' + op[1] + ', 0x' + op[2:],
    (0x7000, 0xF000): lambda op: 'ADD V' + op[1] + ', 0x' + op[2:],
    (0x8000, 0xF00F): lambda op: 'LD V' + op[1] + ', V' + op[2],
    (0x8001, 0xF00F): lambda op: 'OR V' + op[1] + ', V' + op[2],
    (0x8002, 0xF00F): lambda op: 'AND V' + op[1] + ', V' + op[2],
    (0x8003, 0xF00F): lambda op: 'XOR V' + op[1] + ', V' + op[2],
    (0x8004, 0xF00F): lambda op: 'ADD V' + op[1] + ', V' + op[2],
    (0x8005, 0xF00F): lambda op: 'SUB V' + op[1] + ', V' + op[2],
    (0x8006, 0xF00F): lambda op: 'SHR V' + op[1] + ', V' + op[2],
    (0x8007, 0xF00F): lambda op: 'SUBN V' + op[1] + ', V' + op[2],
    (0x800E, 0xF00F): lambda op: 'SHL V' + op[1] + ', V' + op[2],
    (0x9000, 0xF00F): lambda op: 'SNE V' + op[1] + ', V' + op[2],
    (0xA000, 0xF000): lambda op: 'LD I, 0x' + op[1:],
    (0xB000, 0xF000): lambda op: 'JP V0, 0x' + op[1:],
    (0xC000, 0xF000): lambda op: 'RND V' + op[1] + ', 0x' + op[2:],
    (0xD000, 0xF000): lambda op: 'DRW V' + op[1] + ', V' + op[2] + ', 0x' + op[3],
    (0xE09E, 0xF0FF): lambda op: 'SKP V' + op[1],
    (0xE0A1, 0xF0FF): lambda op: 'SKNP V' + op[1],
    (0xF007, 0xF0FF): lambda op: 'LD V' + op[1] + ', DT',
    (0xF00A, 0xF0FF): lambda op: 'LD V' + op[1] + ', K',
    (0xF015, 0xF0FF): lambda op: 'LD DT, V' + op[1],
    (0xF018, 0xF0FF): lambda op: 'LD ST, V' + op[1],
    (0xF01E, 0xF0FF): lambda op: 'ADD I, V' + op[1],
    (0xF029, 0xF0FF): lambda op: 'LD F, V' + op[1],
    (0xF033, 0xF0FF): lambda op: 'LD B, V' + op[1],
    (0xF055, 0xF0FF): lambda op: 'LD [I], V' + op[1],
    (0xF065, 0xF0FF): lambda op: 'LD V' + op[1] + ', [I]',
}


def mnemonic(opcode: int):
    for (pattern, mask), instruction in _patterns.items():
        if not (opcode ^ pattern) & mask:
            return instruction(hex(opcode)[2:].zfill(4).upper())


def disassemble(source: IO[bytes]):
    opcode = source.read(2)
    while opcode:
        yield mnemonic(int.from_bytes(opcode, 'big'))
        opcode = source.read(2)


def main(argv: list) -> None:
    if len(argv) != 3:
        print('Usage: python3 disassembler.py <source> <destination>')
    else:
        _, source_path, dest_path = argv
        with open(source_path, 'rb') as source:
            with open(dest_path, 'w+') as dest:
                for opcode in disassemble(source):
                    if opcode is not None:
                        dest.write(opcode + '\n')


if __name__ == '__main__':
    main(sys.argv)