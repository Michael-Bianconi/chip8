import enum, re


class ArgType(enum.Enum):
    V = re.compile('^v0*([0-9a-f])$', re.IGNORECASE)
    DT = re.compile('^(DT)$', re.IGNORECASE)
    ST = re.compile('^(ST)$', re.IGNORECASE)
    I = re.compile('^(I)$', re.IGNORECASE)
    NIBBLE = re.compile('^(?:0x)?0*([0-9a-f])$', re.IGNORECASE)
    BYTE = re.compile('^(?:0x)?0*([0-9a-f]|[0-9a-f]{2})$', re.IGNORECASE)
    ADDR = re.compile('^(?:0x)?0*([0-9a-f]|[0-9a-f]{2}|[0-9a-f]{3})$', re.IGNORECASE)

def get_formats(opcode: str) -> dict:
    opcode = opcode.upper().strip()
    if opcode == 'ADD':
        return (
            {
                'format': [ArgType.I, ArgType.V],
                'assemble': lambda args: 0xf01e | (args[2] << 8)
            }, {
                'format': [ArgType.V, ArgType.BYTE],
                'assemble': lambda args: 0x7000 | (args[1] << 8) | (args[2])
            }, {
                'format': [ArgType.V, ArgType.V],
                'assemble': lambda args: 0x8004 | (args[1] << 8) | (args[2] << 4)
            }
        )
    elif opcode == 'AND':
        return (
            {
                'format': [ArgType.V, ArgType.V],
                'assemble': lambda args: 0x8002 | (args[1] << 2) | (args[2] << 1)
            }
        )
    elif opcode == 'CALL':
        return (
            {
                'format': [ArgType.ADDR],
                'assemble': lambda args: 0x2000 | args[1]
            }
        )
    else:
        return None



def parse(line: str, *expected_args: ArgType) -> list:
    retval = []
    line = line.split('#',1)[0]
    opcode, args = line.strip().split(' ', 1)
    args = args.split(',')

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


def assemble(line: str) -> int:
    opcode = line.split(' ', 1)[0]
    formats = get_formats(opcode)
    for format in formats:
        args = parse(line, *format['format'])
        if args is not None:
            return format['assemble'](args)
    return None
