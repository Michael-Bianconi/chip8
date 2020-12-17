class Disassembler {

    private static readonly INSTRUCTION_TABLE: [number, number, (s: string) => string][] = [
        [0x00E0, 0xFFFF, (_op: string) => 'CLS'],
        [0x00EE, 0xFFFF, (_op: string) => 'RET'],
        [0x0000, 0xF000, (op: string) => 'SYS 0X' + op.slice(1)],
        [0x1000, 0xF000, (op: string) => 'JP 0X' + op.slice(1)],
        [0x2000, 0xF000, (op: string) => 'CALL 0X' + op.slice(1)],
        [0x3000, 0xF000, (op: string) => 'SE V' + op[1] + ', 0X' + op.slice(2)],
        [0x4000, 0xF000, (op: string) => 'SNE V' + op[1] + ', 0X' + op.slice(2)],
        [0x5000, 0xF00F, (op: string) => 'SE V' + op[1] + ', V' + op[2]],
        [0x6000, 0xF000, (op: string) => 'LD V' + op[1] + ', 0X' + op.slice(2)],
        [0x7000, 0xF000, (op: string) => 'ADD V' + op[1] + ', 0X' + op.slice(2)],
        [0x8000, 0xF00F, (op: string) => 'LD V' + op[1] + ', V' + op[2]],
        [0x8001, 0xF00F, (op: string) => 'OR V' + op[1] + ', V' + op[2]],
        [0x8002, 0xF00F, (op: string) => 'AND V' + op[1] + ', V' + op[2]],
        [0x8003, 0xF00F, (op: string) => 'XOR V' + op[1] + ', V' + op[2]],
        [0x8004, 0xF00F, (op: string) => 'ADD V' + op[1] + ', V' + op[2]],
        [0x8005, 0xF00F, (op: string) => 'SUB V' + op[1] + ', V' + op[2]],
        [0x8006, 0xF00F, (op: string) => 'SHR V' + op[1] + ', V' + op[2]],
        [0x8007, 0xF00F, (op: string) => 'SUBN V' + op[1] + ', V' + op[2]],
        [0x800E, 0xF00F, (op: string) => 'SHL V' + op[1] + ', V' + op[2]],
        [0x9000, 0xF00F, (op: string) => 'SNE V' + op[1] + ', V' + op[2]],
        [0xA000, 0xF000, (op: string) => 'LD I, 0X' + op.slice(1)],
        [0xB000, 0xF000, (op: string) => 'JP V0, 0X' + op.slice(1)],
        [0xC000, 0xF000, (op: string) => 'RND V' + op[1] + ', 0X' + op.slice(2)],
        [0xD000, 0xF000, (op: string) => 'DRW V' + op[1] + ', V' + op[2] + ', 0X' + op[3]],
        [0xE09E, 0xF0FF, (op: string) => 'SKP V' + op[1]],
        [0xE0A1, 0xF0FF, (op: string) => 'SKNP V' + op[1]],
        [0xF007, 0xF0FF, (op: string) => 'LD V' + op[1] + ', DT'],
        [0xF00A, 0xF0FF, (op: string) => 'LD V' + op[1] + ', K'],
        [0xF015, 0xF0FF, (op: string) => 'LD DT, V' + op[1]],
        [0xF018, 0xF0FF, (op: string) => 'LD ST, V' + op[1]],
        [0xF01E, 0xF0FF, (op: string) => 'ADD I, V' + op[1]],
        [0xF029, 0xF0FF, (op: string) => 'LD F, V' + op[1]],
        [0xF033, 0xF0FF, (op: string) => 'LD B, V' + op[1]],
        [0xF055, 0xF0FF, (op: string) => 'LD [I], V' + op[1]],
        [0xF065, 0xF0FF, (op: string) => 'LD V' + op[1] + ', [I]']
    ];

    public static disassemble(opcode: number): string | null {
        for (let format of Disassembler.INSTRUCTION_TABLE) {
            let pattern = format[0];
            let mask = format[1];
            let conversion = format[2];
            if (!((opcode ^ pattern) & mask)) {
                return conversion(opcode.toString(16).toUpperCase());
            }
        }
        return null;
    }
}

try {
    module.exports = Disassembler;
} catch (e) {
    // Do nothing
}