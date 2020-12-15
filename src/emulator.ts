class Emulator {

    static readonly MEMORY_SIZE: number = 0x1000;
    static readonly STACK_SIZE: number = 16;
    static readonly V_REGISTER_COUNT: number = 16;
    static readonly DISPLAY_WIDTH: number = 64;
    static readonly DISPLAY_HEIGHT: number = 32;
    static readonly MOD_4_BIT = 0x10;
    static readonly MOD_8_BIT = 0x100;
    static readonly MOD_12_BIT = 0x1000;
    static readonly MOD_16_BIT = 0x10000;
    static readonly FONT_SIZE = 0x5;
    static readonly FONT_DATA = [
        0xF0, 0x90, 0x90, 0x90, 0xF0,  // 0 @ 0x00 - 0x04
        0x20, 0x60, 0x20, 0x20, 0x70,  // 1 @ 0x05 - 0x09
        0xF0, 0x10, 0xF0, 0x80, 0xF0,  // 2 @ 0x0A - 0x0E
        0xF0, 0x10, 0xF0, 0x10, 0xF0,  // 3 @ 0x0F - 0x13
        0x90, 0x90, 0xF0, 0x10, 0x10,  // 4 @ 0x14 - 0x19
        0xF0, 0x80, 0xF0, 0x10, 0xF0,  // 5 @ 0x1A - 0x1E
        0xF0, 0x80, 0xF0, 0x90, 0xF0,  // 6 @ 0x1F - 0x23
        0xF0, 0x10, 0x20, 0x40, 0x40,  // 7 @ 0x24 - 0x29
        0xF0, 0x90, 0xF0, 0x90, 0xF0,  // 8 @ 0x2A - 0x2E
        0xF0, 0x90, 0xF0, 0x10, 0xF0,  // 9 @ 0x2F - 0x33
        0xF0, 0x90, 0xF0, 0x90, 0x90,  // A @ 0x34 - 0x39
        0xE0, 0x90, 0xE0, 0x90, 0xE0,  // B @ 0x3A - 0x3E
        0xF0, 0x80, 0x80, 0x80, 0xF0,  // C @ 0x3F - 0x43
        0xE0, 0x90, 0x90, 0x90, 0xE0,  // D @ 0x44 - 0x49
        0xF0, 0x80, 0xF0, 0x80, 0xF0,  // E @ 0x4A - 0x4E
        0xF0, 0x80, 0xF0, 0x80, 0x80   // F @ 0x4F - 0x53
    ];

    private static readonly INSTRUCTION_TABLE: [number, number, (e: Emulator, op: number) => void][] = [
        [0x00E0, 0xFFFF, (e, op) => e.cls()],
        [0x00EE, 0xFFFF, (e, op) => e.ret()],
        [0x0000, 0xF000, (e, op) => e.sys_addr()],
        [0x1000, 0xF000, (e, op) => e.jp_addr(op & 0x0FFF)],
        [0x2000, 0xF000, (e, op) => e.call_addr(op & 0xFFF)],
        [0x3000, 0xF000, (e, op) => e.se_v_byte((op & 0x0F00) >> 8, op & 0x00FF)],
        [0x4000, 0xF000, (e, op) => e.sne_v_byte((op & 0x0F00) >> 8, op & 0x00FF)],
        [0x5000, 0xF00F, (e, op) => e.se_v_v((op & 0x0F00) >> 8, (op & 0x00F0) >> 4)],
        [0x6000, 0xF000, (e, op) => e.ld_v_byte((op & 0x0F00) >> 8, op & 0x00FF)],
        [0x7000, 0xF000, (e, op) => e.add_v_byte((op & 0x0F00) >> 8, op & 0x00FF)],
        [0x8000, 0xF00F, (e, op) => e.ld_v_v((op & 0x0F00) >> 8, (op & 0x00F0) >> 4)],
        [0x8001, 0xF00F, (e, op) => e.or_v_v((op & 0x0F00) >> 8, (op & 0x00F0) >> 4)],
        [0x8002, 0xF00F, (e, op) => e.and_v_v((op & 0x0F00) >> 8, (op & 0x00F0) >> 4)],
        [0x8003, 0xF00F, (e, op) => e.xor_v_v((op & 0x0F00) >> 8, (op & 0x00F0) >> 4)],
        [0x8004, 0xF00F, (e, op) => e.add_v_v((op & 0x0F00) >> 8, (op & 0x00F0) >> 4)],
        [0x8005, 0xF00F, (e, op) => e.sub_v_v((op & 0x0F00) >> 8, (op & 0x00F0) >> 4)],
        [0x8006, 0xF00F, (e, op) => e.shr_v((op & 0x0F00) >> 8)],
        [0x8007, 0xF00F, (e, op) => e.subn_v_v((op & 0x0F00) >> 8, (op & 0x00F0) >> 4)],
        [0x800E, 0xF00F, (e, op) => e.shl_v((op & 0x0F00) >> 8)],
        [0x9000, 0xF00F, (e, op) => e.sne_v_v((op & 0x0F00) >> 8, (op & 0x00F0) >> 4)],
        [0xA000, 0xF000, (e, op) => e.ld_i_addr(op & 0x0FFF)],
        [0xB000, 0xF000, (e, op) => e.jp_v0_addr(op & 0x0FFF)],
        [0xC000, 0xF000, (e, op) => e.rnd_v_byte((op & 0x0F00) >> 8, op & 0x00FF)],
        [0xD000, 0xF000, (e, op) => e.drw((op & 0x0F00) >> 8, (op & 0x00F0) >> 4, op & 0x000F)],
        [0xE09E, 0xF0FF, (e, op) => e.skp_v((op & 0x0F00) >> 8)],
        [0xE0A1, 0xF0FF, (e, op) => e.sknp_v((op & 0x0F00) >> 8)],
        [0xF007, 0xF0FF, (e, op) => e.ld_v_dt((op & 0x0F00) >> 8)],
        [0xF00A, 0xF0FF, (e, op) => e.ld_v_k((op & 0x0F00) >> 8)],
        [0xF015, 0xF0FF, (e, op) => e.ld_dt_v((op & 0x0F00) >> 8)],
        [0xF018, 0xF0FF, (e, op) => e.ld_st_v((op & 0x0F00) >> 8)],
        [0xF01E, 0xF0FF, (e, op) => e.add_i_v((op & 0x0F00) >> 8)],
        [0xF029, 0xF0FF, (e, op) => e.ld_f_v((op & 0x0F00) >> 8)],
        [0xF033, 0xF0FF, (e, op) => e.ld_b_v((op & 0x0F00) >> 8)],
        [0xF055, 0xF0FF, (e, op) => e.ld_i_v((op & 0x0F00) >> 8)],
        [0xF065, 0xF0FF, (e, op) => e.ld_v_i((op & 0x0F00) >> 8)],
    ];

    public vRegisters: number[] = Array(Emulator.V_REGISTER_COUNT).fill(0);
    public iRegister: number = 0;
    public dtRegister: number = 0;
    public stRegister: number = 0;
    public stackPointer: number = 0;
    public memory: number[] = Array(Emulator.MEMORY_SIZE).fill(0);
    public programCounter: number = 0x200;
    public stack: number[] = Array(Emulator.STACK_SIZE).fill(0);
    public display: boolean[][] = Emulator.empty_display();
    public unflushedPixels: [number, number, boolean][] = [];
    public wait_for_keypress: boolean = false;
    public store_keypress_in: number = null;
    public paused: boolean = false;
    public breakpoints: number[] = [];

    next(): void {
        if (!this.breakpoints.includes(this.programCounter)) {
            let opcode = this.get_instruction();
            for (let i = 0; i < Emulator.INSTRUCTION_TABLE.length; i++) {
                let [pattern, mask, operation] = Emulator.INSTRUCTION_TABLE[i];
                if (!((opcode ^ pattern) & mask)) {
                    operation(this, opcode);
                    break;
                }
            }
        }
    }

    // TODO Unit test
    cls(): void {
        for (let y = 0; y < this.display.length; y++) {
            for (let x = 0; x < this.display[y].length; x++) {
                if (this.display[y][x]) {
                    this.display[y][x] = false;
                    this.unflushedPixels.push([x, y, false]);
                }
            }
        }
        this.increment_program_counter();
    }

    // TODO Unit test
    ret(): void {
        this.programCounter = this.stack[this.stackPointer];
        this.stackPointer = (this.stackPointer - 1) % Emulator.MOD_4_BIT;
    }

    // TODO Unit test
    sys_addr() {
        // Unused
        this.increment_program_counter();
    }

    // TODO Unit test
    jp_addr(address: number) {
        this.programCounter = address;
    }

    // TODO Unit test
    call_addr(address: number): void {
        this.stackPointer = (this.stackPointer + 1) % Emulator.MOD_4_BIT;
        this.stack[this.stackPointer] = this.programCounter;
        this.programCounter = address;
    }

    se_v_byte(vx: number, byte: number): void {
        let jump = this.vRegisters[vx] === byte;
        this.increment_program_counter(jump ? 2 : 1);
    }

    sne_v_byte(vx: number, byte: number): void {
        let jump = this.vRegisters[vx] !== byte;
        this.increment_program_counter(jump ? 2 : 1);
    }

    se_v_v(vx: number, vy: number): void {
        let jump = this.vRegisters[vx] === this.vRegisters[vy];
        this.increment_program_counter(jump ? 2 : 1);
    }

    ld_v_byte(vx: number, byte: number): void {
        this.vRegisters[vx] = byte;
        this.increment_program_counter();
    }

    add_v_byte(vx: number, byte: number): void {
        this.vRegisters[vx] = (this.vRegisters[vx] + byte) % Emulator.MOD_8_BIT;
        this.increment_program_counter()
    }

    ld_v_v(vx: number, vy: number): void {
        this.vRegisters[vx] = this.vRegisters[vy];
        this.increment_program_counter();
    }

    or_v_v(vx: number, vy: number): void {
        this.vRegisters[vx] |= this.vRegisters[vy];
        this.increment_program_counter();
    }

    and_v_v(vx: number, vy: number): void {
        this.vRegisters[vx] &= this.vRegisters[vy];
        this.increment_program_counter();
    }

    xor_v_v(vx: number, vy: number): void {
        this.vRegisters[vx] ^= this.vRegisters[vy];
        this.increment_program_counter();
    }

    add_v_v(vx: number, vy: number): void {
        this.vRegisters[vx] = (this.vRegisters[vx] + this.vRegisters[vy]) % Emulator.MOD_8_BIT;
        this.increment_program_counter();
    }

    sub_v_v(vx: number, vy: number): void {
        this.vRegisters[0xF] = this.vRegisters[vx] > this.vRegisters[vy] ? 1 : 0;
        this.vRegisters[vx] = ((this.vRegisters[vx] - this.vRegisters[vy]) >>> 0) % Emulator.MOD_8_BIT;
        this.increment_program_counter();
    }

    shr_v(vx: number): void {
        this.vRegisters[0xF] = this.vRegisters[vx] & 0x1;
        this.vRegisters[vx] >>= 1;
        this.increment_program_counter();
    }

    subn_v_v(vx: number, vy: number): void {
        this.vRegisters[0xF] = this.vRegisters[vy] > this.vRegisters[vx] ? 1 : 0;
        this.vRegisters[vx] = ((this.vRegisters[vy] - this.vRegisters[vx]) >>> 0) % Emulator.MOD_8_BIT;
        this.increment_program_counter();
    }

    shl_v(vx: number): void {
        this.vRegisters[0xF] = (this.vRegisters[vx] & 0x80) >> 7;
        this.vRegisters[vx] = (this.vRegisters[vx] << 1) % Emulator.MOD_8_BIT;
        this.increment_program_counter();
    }

    // TODO Unit test
    sne_v_v(vx: number, vy: number): void {
        let jump = this.vRegisters[vx] !== this.vRegisters[vy];
        this.increment_program_counter(jump ? 2 : 1);
    }

    // TODO Unit test
    ld_i_addr(addr: number): void {
        this.iRegister = addr;
        this.increment_program_counter();
    }

    // TODO Unit test
    jp_v0_addr(addr: number): void {
        this.programCounter = this.vRegisters[0] + addr;
        this.increment_program_counter();
    }

    // TODO Unit test
    rnd_v_byte(vx: number, byte: number): void {
        this.vRegisters[vx] = Math.floor(Math.random() * Math.floor(0x100)) & byte;
        this.increment_program_counter();
    }

    // TODO Unit test
    drw(vx: number, vy: number, height: number): void {
        for (let row = 0; row < height; row++) {
            let sprite: number = this.memory[this.iRegister + row];
            for (let col = 0; col < 8; col++) {
                let x: number = (this.vRegisters[vx] + col) % Emulator.DISPLAY_WIDTH;
                let y: number = (this.vRegisters[vy] + row) % Emulator.DISPLAY_HEIGHT;
                let pixel: boolean = (sprite & (0x80 >> col)) > 0;
                let current: boolean = this.display[y][x];
                if (current !== pixel) {
                    this.unflushedPixels.push([x, y, pixel]);
                } else if (current && pixel) {
                    this.vRegisters[0xF] = 1;  // collision
                }
                this.display[y][x] = current !== pixel;
            }
        }
        this.increment_program_counter();
    }

    // TODO unit tests
    skp_v(vx: number): void {
        // TODO
        this.increment_program_counter();
    }

    // TODO unit tests
    sknp_v(vx: number): void {
        // TODO
        this.increment_program_counter();
    }

    // TODO unit test
    ld_v_dt(vx: number): void {
        this.vRegisters[vx] = this.dtRegister;
        this.increment_program_counter();
    }

    // TODO unit test
    ld_v_k(vx: number): void {
        // TODO
        this.increment_program_counter();
    }

    // TODO unit test
    ld_dt_v(vx: number): void {
        this.dtRegister = this.vRegisters[vx];
        this.increment_program_counter();
    }

    // TODO unit test
    ld_st_v(vx: number): void {
        this.stRegister = this.vRegisters[vx];
        this.increment_program_counter();
    }

    // TODO unit test
    add_i_v(vx: number): void {
        this.iRegister = (this.iRegister + this.vRegisters[vx]) % Emulator.MOD_8_BIT;
        this.increment_program_counter();
    }

    // TODO unit test
    ld_f_v(vx: number): void {
        this.iRegister = this.vRegisters[vx] * Emulator.FONT_SIZE;
        this.increment_program_counter();
    }

    // TODO unit test
    ld_b_v(vx: number): void {
        this.memory[this.iRegister] = this.vRegisters[vx]; // 100
        this.memory[this.iRegister + 1] = this.vRegisters[vx] % 100; // 10
        this.memory[this.iRegister + 2] = this.vRegisters[vx] % 10;
        this.increment_program_counter();
    }

    // TODO unit test
    ld_i_v(vx: number): void {
        for (let i = 0; i <= vx; i++) {
            this.memory[this.iRegister + i] = this.vRegisters[i];
        }
        this.increment_program_counter();
    }

    // TODO unit test
    ld_v_i(vx: number): void {
        for (let i = 0; i <= vx; i++) {
            this.vRegisters[i] = this.memory[this.iRegister + i];
        }
        this.increment_program_counter();
    }

    increment_program_counter(n: number = 1) {
        this.programCounter += n * 2;
    }

    get_instruction() {
        let [upper, lower] = this.memory.slice(this.programCounter, this.programCounter + 2);
        return (upper << 8) | lower;
    }

    setBreakpoint(address: number): boolean {
        if (address >= 0 && address <= 0xFFF) {
            this.breakpoints.push(address);
            return true;
        }
        return false;
    }

    removeBreakpoint(address: number): void {
        let index = this.breakpoints.indexOf(address);
        if (index !== -1) {
            this.breakpoints.splice(index, 1);
        }
    }

    set_by_name(register: string, value: number): boolean {
        register = register.toUpperCase();
        if (register.startsWith('V')) {
            let index = parseInt(register[1], 16);
            this.vRegisters[index] = value % Emulator.MOD_8_BIT;
        } else if (register === 'I') {
            this.iRegister = value % Emulator.MOD_16_BIT;
        } else if (register === 'DT') {
            this.dtRegister = value % Emulator.MOD_8_BIT;
        } else if (register === 'ST') {
            this.stRegister = value % Emulator.MOD_8_BIT;
        } else if (register === 'SP') {
            this.stackPointer = value % Emulator.MOD_8_BIT;
        } else if (register === 'PC') {
            this.programCounter = value % Emulator.MOD_12_BIT;
        } else {
            return false;
        }

        return true;
    }

    multibyte_memory_write(address: number, value: number): boolean {
        if (address >= 0 && value >= 0) {
            while (value !== 0) {
                this.memory[address++] = value & 0xFF;
                value >>= 8;
            }
            return true;
        }
        return false;
    }

    stack_write(index: number, value: number): void {
        this.stack[index % Emulator.STACK_SIZE] = value % Emulator.MOD_16_BIT;
    }

    static init_memory(): number[] {
        let memory: number[] = Array(Emulator.MEMORY_SIZE).fill(0);
        memory = Emulator.FONT_DATA.concat(memory.slice(Emulator.FONT_DATA.length));
        return memory;
    }

    static empty_display(): boolean[][] {
        let display: boolean[][] = Array(Emulator.DISPLAY_HEIGHT);
        for (let row = 0; row < display.length; row++) {
            display[row] = Array(Emulator.DISPLAY_WIDTH).fill(false);
        }
        return display;
    }

    read_on_change(inputElement: HTMLInputElement): void {
        let emulator = this;
        inputElement.addEventListener('change', function() {
            let reader = new FileReader();
            reader.onload = e => {
                let array = new Uint8Array(<ArrayBuffer> e.target.result);
                for (let i = 0; i < array.length; i++) {
                    emulator.memory[emulator.programCounter + i] = array[i];
                }
            };
            reader.readAsArrayBuffer(this.files[0]);

        }, false);
    }
}

try {
    module.exports = Emulator;
} catch (e) {
    // Do nothing
}