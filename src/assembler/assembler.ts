class Assembler {

    private static readonly INSTRUCTIONS: Record<string, [((operand: string) => (string | number))[], ((...v: any[]) => number)][]> = {
        'ADD': [
            [[Assembler.parseI, Assembler.parseV], (_i: any, vx: number) => 0xF01E | (vx << 8)],
            [[Assembler.parseV, Assembler.parseByte], (vx: number, byte: number) => 0x7000 | (vx << 8) | (byte)],
            [[Assembler.parseV, Assembler.parseV], (vx: number, vy: number) => 0x8004 | (vx << 8) | (vy << 4)]],
        'AND': [
            [[Assembler.parseV, Assembler.parseV], (vx: number, vy: number) => 0x8002 | (vx << 8) | (vy << 4)]],
        'CALL': [
            [[Assembler.parseAddress], (addr: number) => 0x2000 | addr]],
        'CLS': [
            [[], () => 0x00E0]],
        'DRW': [
            [[Assembler.parseV, Assembler.parseV, Assembler.parseNibble], (vx: number, vy: number, n: number) => 0xD000 | (vx << 8) | (vy << 4) | n]],
        'JP': [
            [[Assembler.parseAddress], (addr: number) => 0x1000 | addr],
            [[Assembler.parseV0, Assembler.parseAddress], (_v0: any, addr: number) => 0xB000 | addr]],
        'LD': [
            [[Assembler.parseB, Assembler.parseV], (_b: any, v: number) => 0xF033 | (v << 8)],
            [[Assembler.parseDT, Assembler.parseV], (_dt: any, v: number) => 0xF015 | (v << 8)],
            [[Assembler.parseF, Assembler.parseV], (_f: any, v: number) => 0xF029 | (v << 8)],
            [[Assembler.parseI, Assembler.parseAddress], (_i: any, addr: number) => 0xA000 | addr],
            [[Assembler.parseAI, Assembler.parseV], (_ai: any, v: number) => 0xF055 | (v << 8)],
            [[Assembler.parseST, Assembler.parseV], (_st: any, v: number) => 0xF018 | (v << 8)],
            [[Assembler.parseV, Assembler.parseByte], (v: number, byte: number) => 0x6000 | (v << 8) | byte],
            [[Assembler.parseV, Assembler.parseDT], (v: number, _dt: any) => 0xF007 | (v << 8)],
            [[Assembler.parseV, Assembler.parseAI], (v: number, _ai: any) => 0xF065 | (v << 8)],
            [[Assembler.parseV, Assembler.parseK], (v: number, _k: any) => 0xF00A | (v << 8)],
            [[Assembler.parseV, Assembler.parseV], (vx: number, vy: number) => 0x8000 | (vx << 8) | (vy << 4)]],
        'OR': [
            [[Assembler.parseV, Assembler.parseV], (vx: number, vy: number) => 0x8001 | (vx << 8) | (vy << 4)]],
        'RET': [
            [[], () => 0x00EE]],
        'RND': [
            [[Assembler.parseV, Assembler.parseByte], (v: number, byte: number) => 0xC000 | (v << 8) | byte]],
        'SE': [
            [[Assembler.parseV, Assembler.parseByte], (v: number, byte: number) => 0x3000 | (v << 8) | byte],
            [[Assembler.parseV, Assembler.parseV], (vx: number, vy: number) => 0x5000 | (vx << 8) | (vy << 4)]],
        'SHL': [
            [[Assembler.parseV], (v: number) => 0x800E | (v << 8)],
            [[Assembler.parseV, Assembler.parseV], (vx: number, vy: number) => 0x800E | (vx << 8) | (vy << 4)]],
        'SHR': [
            [[Assembler.parseV], (v: number) => 0x8006 | (v << 8)],
            [[Assembler.parseV, Assembler.parseV], (vx: number, vy: number) => 0x8006 | (vx << 8) | (vy << 4)]],
        'SKNP': [
            [[Assembler.parseV], (v: number) => 0xE0A1 | (v << 8)]],
        'SKP': [
            [[Assembler.parseV], (v: number) => 0xE09E | (v << 8)]],
        'SNE': [
            [[Assembler.parseV, Assembler.parseByte], (v: number, byte: number) => 0x4000 | (v << 8) | byte],
            [[Assembler.parseV, Assembler.parseV], (vx: number, vy: number) => 0x9000 | (vx << 8) | (vy << 4)]],
        'SUB': [
            [[Assembler.parseV, Assembler.parseV], (vx: number, vy: number) => 0x8005 | (vx << 8) | (vy << 4)]],
        'SUBN': [
            [[Assembler.parseV, Assembler.parseV], (vx: number, vy: number) => 0x8007 | (vx << 8) | (vy << 4)]],
        'SYS': [
            [[Assembler.parseAddress], (addr: number) => addr]],
        'XOR': [
            [[Assembler.parseV, Assembler.parseV], (vx: number, vy: number) => 0x8003 | (vx << 8) | (vy << 4)]],
    };

    public static assembleLines(lines: string[]): number[] | null {
        let result = [];
        for (let line of lines) {
            let opcode = Assembler.assembleLine(line);
            if (opcode === null) {
                return null;
            } else {
                result.push(opcode);
            }
        }
        return result;
    }

    public static assembleLine(line: string): number | null {
        let [mnemonic, operands] = Assembler.splitMnemonic(line);
        return Assembler.toOpcode(mnemonic, operands);
    }

    private static toOpcode(mnemonic: string, operands: string[]): number {
        let formats = Assembler.INSTRUCTIONS[mnemonic];
        if (formats !== undefined) {
            for (let format of formats) {
                let [expectedOperands, conversion] = format;
                let parsedOperands = Assembler.parse(operands, expectedOperands);
                if (parsedOperands !== null && parsedOperands !== undefined) {
                    return conversion(...parsedOperands);
                }
            }
        }
        return null;
    }

    private static parse(operands: string[], parsers: ((s: string) => (string | number))[]): (string | number)[] | null {
        if (operands.length === parsers.length) {
            let ops: (string | number)[] = [];
            for (let i = 0; i < operands.length; i++) {
                ops.push(parsers[i](operands[i]));
                if (ops[i] === null) {
                    return null;
                }
            }
            return ops;
        }
    }


    private static parseV(operand: string): string | number {
        let match = operand.match(/^V([0-9A-F])$/);
        return match !== null ? parseInt(match[1], 16) : null;
    }

    private static parseV0(operand: string): string | number {
        return Assembler.parseLiteral('V0', operand);
    }

    private static parseI(operand: string): string | number {
        return Assembler.parseLiteral('I', operand);
    }

    private static parseB(operand: string): string | number {
        return Assembler.parseLiteral('B', operand);
    }

    private static parseF(operand: string): string | number {
        return Assembler.parseLiteral('F', operand);
    }

    private static parseDT(operand: string): string | number {
        return Assembler.parseLiteral('DT', operand);
    }

    private static parseST(operand: string): string | number {
        return Assembler.parseLiteral('ST', operand);
    }

    private static parseK(operand: string): string | number {
        return Assembler.parseLiteral('K', operand);
    }

    private static parseAI(operand: string): string | number {
        return Assembler.parseLiteral('[I]', operand);
    }

    private static parseNibble(operand: string): string | number {
        let value = parseInt(operand);
        return !isNaN(value) && 0 <= value && value <= 0xF ? value : null;
    }

    private static parseByte(operand: string): string | number {
        let value = parseInt(operand);
        return !isNaN(value) && 0 <= value && value <= 0xFF ? value : null;
    }

    private static parseAddress(operand: string): string | number {
        let value = parseInt(operand);
        return !isNaN(value) && 0 <= value && value <= 0xFFF ? value : null;
    }

    private static parseLiteral(literal: string, operand: string): string | number {
        return operand === literal ? operand : null;
    }

    /**
     * @param line Uppercase, no label, no define, no comment, not empty
     * @returns [opcode, [operands]]
     */
    static splitMnemonic(line: string): [string, string[]] {
        let opEnd = line.indexOf(' ');
        if (opEnd !== -1) {
            let [opcode, operands] = [line.slice(0, opEnd).trim(), line.slice(opEnd).trim()];
            return [opcode, operands.split(/\s*,\s*/).map(o => o.trim())];
        } else {
            return [line, []];
        }
    }
}

try {
    module.exports = Assembler;
} catch (e) {
    // Do nothing
}