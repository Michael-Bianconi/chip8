import string
import sys

_patterns = {
    '00E0': lambda op: 'CLS',
    '00EE': lambda op: 'RET',
    '0nnn': lambda op: 'SYS 0x' + op[1:],
    '1nnn': lambda op: 'JP 0x' + op[1:],
    '2nnn': lambda op: 'CALL 0x' + op[1:],
    '3xkk': lambda op: 'SE V' + op[1] + ', 0x' + op[2:],
    '4xkk': lambda op: 'SNE V' + op[1] + ', 0x' + op[2:],
    '5xy0': lambda op: 'SE V' + op[1] + ', V' + op[2],
    '6xkk': lambda op: 'LD V' + op[1] + ', 0x' + op[2:],
    '7xkk': lambda op: 'ADD V' + op[1] + ', 0x' + op[2:],
    '8xy0': lambda op: 'LD V' + op[1] + ', 0x' + op[2:],
    '8xy1': lambda op: 'OR V' + op[1] + ', 0x' + op[2:],
    '8xy2': lambda op: 'AND V' + op[1] + ', 0x' + op[2:],
    '8xy3': lambda op: 'XOR V' + op[1] + ', 0x' + op[2:],
    '8xy4': lambda op: 'ADD V' + op[1] + ', 0x' + op[2:],
    '8xy5': lambda op: 'SUB V' + op[1] + ', 0x' + op[2:],
    '8xy6': lambda op: 'SHR V' + op[1] + ', 0x' + op[2:],
    '8xy7': lambda op: 'SUBN V' + op[1] + ', 0x' + op[2:],
    '8xyE': lambda op: 'SHL V' + op[1] + ', 0x' + op[2:],
    '9xy0': lambda op: 'SNE V' + op[1] + ', 0x' + op[2:],
    'Annn': lambda op: 'LD I, 0x' + op[1:],
    'Bnnn': lambda op: 'JP V0, 0x' + op[1:],
    'Cxkk': lambda op: 'RND V' + op[1] + ', 0x' + op[2:],
    'Dxyn': lambda op: 'DRW V' + op[1] + ', V' + op[2] + ', 0x' + op[3],
    'Ex9E': lambda op: 'SKP V' + op[1],
    'ExA1': lambda op: 'SKNP V' + op[1],
    'Fx07': lambda op: 'LD V' + op[1] + 'DT',
    'Fx0A': lambda op: 'LD V' + op[1] + 'K',
    'Fx15': lambda op: 'LD DT, V' + op[1],
    'Fx18': lambda op: 'LD ST, V' + op[1],
    'Fx1E': lambda op: 'ADD I, V' + op[1],
    'Fx29': lambda op: 'LD F, V' + op[1],
    'Fx33': lambda op: 'LD B, V' + op[1],
    'Fx55': lambda op: 'LD [I], V' + op[1],
    'Fx65': lambda op: 'LD V' + op[1] + ' [I]',
}


def mnemonic(opcode: str):
    for key, value in _patterns.items():
        if all([opcode[i] == key[i] for i in range(len(key)) if key[i] in string.hexdigits]):
            return value(opcode)


def disassemble(source):
    opcode = source.read(2)
    if opcode:
        yield mnemonic(opcode.hex().upper())


def main(argv: list) -> None:
    if len(argv) != 3:
        print('Usage: python3 disassembler.py <source> <destination>')
    else:
        _, source_path, dest_path = argv
        with open(source_path, 'rb') as source:
            for opcode in disassemble(source):
                print(opcode)


if __name__ == '__main__':
    main(sys.argv)