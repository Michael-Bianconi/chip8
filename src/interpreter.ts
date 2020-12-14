class Interpreter {

    private readonly emulator: Emulator;
    private static readonly HELP_TEXT = [
        'Chip-8 Interpreter',
        'HELP: Show help text',
        'RUN: Start (or resume) emulation',
        'SET (<register> | mem[<i>] | stack[<i>]) <value>: Set data to value',
        'BREAKPOINT <address>: Pause emulator when the program counter reaches this point',
        'NOBREAKPOINT <address>: Remove breakpoint at given address',
        'STEP: Execute the current instruction',
    ];
    private static readonly INVALID_BREAKPOINT = [
        'Breakpoints must be in the range of [0, 0xFFF]'
    ];
    private static readonly UNKNOWN_COMMAND = [
        'Unknown command. Type HELP for options.'
    ];

    constructor(emulator: Emulator) {
        this.emulator = emulator;
    }

    interpret(value: string): string[] {
        value = value.toUpperCase().trim();
        if (value === 'HELP') {
            return Interpreter.HELP_TEXT;
        }
        if (value === 'RUN') {
            this.emulator.paused = false;
            return [];
        }
        if (value === 'STEP') {
            if (!this.emulator.wait_for_keypress) {
                this.emulator.next();
            }
        }

        let breakpoint = Interpreter.checkBreakpoint(value);
        if (breakpoint !== null) {
            if (this.emulator.setBreakpoint(breakpoint)) {
                return [];
            } else {
                return Interpreter.INVALID_BREAKPOINT;
            }
        }

        let nobreakpoint = Interpreter.checkBreakpoint(value, true);
        if (nobreakpoint !== null) {
            this.emulator.removeBreakpoint(nobreakpoint);
            return [];
        }

        let setReg = Interpreter.checkSetRegister(value);
        if (setReg !== null) {
            this.emulator.set_by_name(setReg[0], setReg[1]);
            return [];
        }

        let setMem = Interpreter.checkSetMemory(value);
        if (setMem !== null) {
            this.emulator.multibyte_memory_write(setMem[0], setMem[1]);
            return [];
        }

        let setStack = Interpreter.checkSetStack(value);
        if (setStack !== null) {
            this.emulator.stack_write(setStack[0], setStack[1]);
            return [];
        }

        return Interpreter.UNKNOWN_COMMAND;
    }

    private static checkBreakpoint(userInput: string, no: boolean = false): number {
        let breakpointPattern = /BREAKPOINT\s+((0X)?[0-9A-F]+)/;
        let noBreakpointPattern = /NOBREAKPOINT\s+((0X)?[0-9A-F]+)/;
        let breakpointMatch = userInput.match(no ? noBreakpointPattern : breakpointPattern);
        if (breakpointMatch !== null) {
            return parseInt(breakpointMatch[1], breakpointMatch[2] !== undefined ? 16 : 10);
        } else {
            return null;
        }
    }

    private static checkSetRegister(userInput: string): [string, number] {
        let match = userInput.match(/SET\s+((?:V[0-9A-F])|DT|ST|I|PC|SP)\s+((0x)?[0-9A-F]+)/);
        if (match !== null) {
            let register = match[1];
            let value = parseInt(match[2], match[3] !== undefined ? 16 : 10);
            return [register, value];
        } else {
            return null;
        }
    }

    private static checkSetMemory(userInput: string): [number, number] {
        let match = userInput.match(/SET\s+MEM\[((0x)?[0-9A-F])]\s+((0x)?[0-9A-F]+)/);
        if (match !== null) {
            let address = parseInt(match[1], match[2] !== undefined ? 16 : 10);
            let value = parseInt(match[3], match[4] !== undefined ? 16 : 10);
            return [address, value];
        } else {
            return null;
        }
    }

    private static checkSetStack(userInput: string): [number, number] {
        let match = userInput.match(/SET\s+STACK\[((0x)?[0-9A-F])]\s+((0x)?[0-9A-F]+)/);
        if (match !== null) {
            let address = parseInt(match[1], match[2] !== undefined ? 16 : 10);
            let value = parseInt(match[3], match[4] !== undefined ? 16 : 10);
            return [address, value];
        } else {
            return null;
        }
    }
}

try {
    module.exports = Interpreter;
} catch (e) {
    // Do nothing
}