class Emulator {

    static readonly MEMORY_SIZE: number = 0x1000;
    static readonly STACK_SIZE: number = 16;
    static readonly V_REGISTER_COUNT: number = 16;
    static readonly DISPLAY_WIDTH: number = 64;
    static readonly DISPLAY_HEIGHT: number = 32;
    static readonly MOD_4_BIT = 0x10;
    static readonly MOD_8_BIT = 0x100;
    static readonly MOD_12_BIT = 0x1000;
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

    public v_registers: number[] = Array(Emulator.V_REGISTER_COUNT).fill(0);
    public i_register: number = 0;
    public dt_register: number = 0;
    public st_register: number = 0;
    public stack_pointer: number = 0;
    public memory: number[] = Array(Emulator.MEMORY_SIZE).fill(0);
    public program_counter: number = 0x200;
    public stack: number[] = Array(Emulator.STACK_SIZE).fill(0);
    public display: boolean[][] = Emulator.empty_display();
    public unflushed_pixels: [number, number, boolean][] = [];
    public wait_for_keypress: boolean = false;
    public store_keypress_in: number = null;

    // TODO Unit test
    cls() {
        for (let y = 0; y < this.display.length; y++) {
            for (let x = 0; x < this.display[y].length; x++) {
                if (this.display[y][x]) {
                    this.display[y][x] = false;
                    this.unflushed_pixels.push([x, y, false]);
                }
            }
        }
        this.increment_program_counter();
    }

    // TODO Unit test
    ret() {
        this.program_counter = this.stack[this.stack_pointer];
        this.stack_pointer = (this.stack_pointer - 1) % Emulator.MOD_4_BIT;
    }

    // TODO Unit test
    sys_address() {
        // Unused
        this.increment_program_counter();
    }

    // TODO Unit test
    jp_address(address: number) {
        this.program_counter = address;
    }

    // TODO Unit test
    call_address(address: number): void {
        this.stack_pointer = (this.stack_pointer + 1) % Emulator.MOD_4_BIT;
        this.stack[this.stack_pointer] = this.program_counter;
        this.program_counter = address;
    }

    se_v_byte(vx: number, byte: number): void {
        let jump = this.v_registers[vx] === byte;
        this.increment_program_counter(jump ? 2 : 1);
    }

    sne_v_byte(vx: number, byte: number): void {
        let jump = this.v_registers[vx] !== byte;
        this.increment_program_counter(jump ? 2 : 1);
    }

    se_v_v(vx: number, vy: number): void {
        let jump = this.v_registers[vx] === this.v_registers[vy];
        this.increment_program_counter(jump ? 2 : 1);
    }

    ld_v_byte(vx: number, byte: number): void {
        this.v_registers[vx] = byte;
        this.increment_program_counter();
    }

    add_v_byte(vx: number, byte: number): void {
        this.v_registers[vx] = (this.v_registers[vx] + byte) % Emulator.MOD_8_BIT;
        this.increment_program_counter()
    }

    ld_v_v(vx: number, vy: number): void {
        this.v_registers[vx] = this.v_registers[vy];
        this.increment_program_counter();
    }

    or_v_v(vx: number, vy: number): void {
        this.v_registers[vx] |= this.v_registers[vy];
        this.increment_program_counter();
    }

    and_v_v(vx: number, vy: number): void {
        this.v_registers[vx] &= this.v_registers[vy];
        this.increment_program_counter();
    }

    xor_v_v(vx: number, vy: number): void {
        this.v_registers[vx] ^= this.v_registers[vy];
        this.increment_program_counter();
    }

    add_v_v(vx: number, vy: number): void {
        this.v_registers[vx] = (this.v_registers[vx] + this.v_registers[vy]) % Emulator.MOD_8_BIT;
        this.increment_program_counter();
    }

    sub_v_v(vx: number, vy: number): void {
        this.v_registers[0xF] = this.v_registers[vx] > this.v_registers[vy] ? 1 : 0;
        this.v_registers[vx] = ((this.v_registers[vx] - this.v_registers[vy]) >>> 0) % Emulator.MOD_8_BIT;
        this.increment_program_counter();
    }

    shr_v(vx: number): void {
        this.v_registers[0xF] = this.v_registers[vx] & 0x1;
        this.v_registers[vx] >>= 1;
        this.increment_program_counter();
    }

    subn_v_v(vx: number, vy: number): void {
        this.v_registers[0xF] = this.v_registers[vy] > this.v_registers[vx] ? 1 : 0;
        this.v_registers[vx] = ((this.v_registers[vy] - this.v_registers[vx]) >>> 0) % Emulator.MOD_8_BIT;
        this.increment_program_counter();
    }

    shl_v(vx: number): void {
        this.v_registers[0xF] = (this.v_registers[vx] & 0x80) >> 7;
        this.v_registers[vx] = (this.v_registers[vx] << 1) % Emulator.MOD_8_BIT;
        this.increment_program_counter();
    }

    // TODO Unit test
    sne_v_v(vx: number, vy: number): void {
        let jump = this.v_registers[vx] !== this.v_registers[vy];
        this.increment_program_counter(jump ? 2 : 1);
    }

    // TODO Unit test
    ld_i_addr(addr: number): void {
        this.i_register = addr;
        this.increment_program_counter();
    }

    // TODO Unit test
    jp_v0_addr(addr: number): void {
        this.program_counter = this.v_registers[0] + addr;
        this.increment_program_counter();
    }

    // TODO Unit test
    rnd_v_byte(vx: number, byte: number): void {
        this.v_registers[vx] = Math.floor(Math.random() * Math.floor(0x100)) & byte;
        this.increment_program_counter();
    }

    // TODO Unit test
    drw(vx: number, vy: number, height: number): void {
        for (let row = 0; row < height; row++) {
            let sprite: number = this.memory[this.i_register + row];
            for (let col = 0; col < 8; col++) {
                let x: number = (this.v_registers[vx] + col) % Emulator.DISPLAY_WIDTH;
                let y: number = (this.v_registers[vy] + row) % Emulator.DISPLAY_HEIGHT;
                let pixel: boolean = (sprite & (0x80 >> col)) > 0;
                let current: boolean = this.display[y][x];
                if (current !== pixel) {
                    this.unflushed_pixels.push([x, y, pixel]);
                } else if (current && pixel) {
                    this.v_registers[0xF] = 1;  // collision
                }
                this.display[y][x] = current !== pixel;
            }
        }
        this.increment_program_counter();
    }

    increment_program_counter(n: number = 1) {
        this.program_counter += n * 2;
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

}

module.exports = Emulator;