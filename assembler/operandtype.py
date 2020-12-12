import enum
import re
import string


class OperandType(enum.Enum):

    # Values should be kept in order
    V = 0
    V0 = 1
    B = 2
    F = 3
    DT = 4
    ST = 5
    I = 6
    K = 7
    AI = 8
    NIBBLE = 9
    BYTE = 10
    ADDR = 11

    @staticmethod
    def parse(operand_type, operand: str):
        if operand_type == OperandType.V:
            return OperandType.parse_v(operand)
        elif operand_type == OperandType.NIBBLE:
            return OperandType.parse_nibble(operand)
        elif operand_type == OperandType.BYTE:
            return OperandType.parse_byte(operand)
        elif operand_type == OperandType.ADDR:
            return OperandType.parse_addr(operand)
        elif operand_type == OperandType.AI:
            return OperandType.parse_literal('[I]', operand)
        else:
            return OperandType.parse_literal(operand_type.name, operand)

    @staticmethod
    def parse_literal(value: str, operand: str) -> str:
        pattern = '^(' + re.escape(value) + ')$'
        match = re.match(pattern, operand, re.IGNORECASE)
        return match.group(1).upper() if match is not None else None

    @staticmethod
    def parse_v(operand: str) -> int:
        pattern = r'^v0*([0-9a-fA-F])$'
        match = re.match(pattern, operand, re.IGNORECASE)
        if match is not None:
            return int(match.group(1), 16)

    @staticmethod
    def parse_nibble(operand: str) -> int:
        return OperandType._to_int(operand, (0x0, 0x10))

    @staticmethod
    def parse_byte(operand: str) -> int:
        return OperandType._to_int(operand, (0x0, 0x100))

    @staticmethod
    def parse_addr(operand: str) -> int:
        return OperandType._to_int(operand, (0x0, 0x1000))

    @staticmethod
    def _to_int(value: str, allowed_range: tuple) -> int:

        if value.startswith('0x') or value.startswith('0X'):
            return_value = int(value, 16)
        elif value.startswith('#'):
            return_value = int(value[1:], 16)
        else:
            if all([x.isdigit() for x in value]):
                return_value = int(value, 10)
            else:
                return_value = None

        if return_value is not None and return_value not in range(*allowed_range):
            raise ValueError(f'Expected integer in range {allowed_range}, got [{value}]')
        else:
            return return_value
