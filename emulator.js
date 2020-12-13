class Emulator {

    constructor() {
        this.MEMORY_SIZE = 0x1000;
        this.STACK_SIZE = 16;
        this.V_REGISTER_COUNT = 16;
        this.DISPLAY_WIDTH = 64;
        this.DISPLAY_HEIGHT = 32;
        this.v_registers = Array(this.V_REGISTER_COUNT).fill(0);
        this.i_register = 0;
        this.dt_register = 0;
        this.st_register = 0;
        this.stack_pointer = 0;
        this.memory = Array(this.MEMORY_SIZE).fill(0);
        this.program_counter = 0x200;
        this.stack = Array(this.STACK_SIZE).fill(0);
        this.display = Array(this.DISPLAY_HEIGHT);
        for (let i = 0; i < this.display.length; i++) {
            this.display[i] = Array(this.DISPLAY_WIDTH);
        }
        this.unflushed_pixels = [];
        this.wait_for_keypress = false;
        this.store_keypress_register = null;
        this.memory = Emulator.FONT_DATA.concat(this.memory.slice(Emulator.FONT_DATA.length));
    }

    init_fonts() {
        let i = 0;
        Emulator.FONT_DATA.forEach(f => {
            this.memory[i++] = f;
        });
    };

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

    ret() {
        this.program_counter = this.stack[this.stack_pointer];
        this.stack_pointer = (this.stack_pointer - 1) % Emulator.MOD_4_BIT;
    }

    sys_address() {
        // Unused
        this.increment_program_counter();
    }

    jp_address(address) {
        this.program_counter = address;
    }

    call_address(address) {
        this.stack_pointer = (this.stack_pointer + 1) % Emulator.MOD_4_BIT;
        this.stack[this.stack_pointer] = this.program_counter;
        this.program_counter = address;
    }

    se_v_byte(vx, byte) {
        let jump = this.v_registers[vx] === byte;
        this.increment_program_counter(jump ? 2 : 1);
    }

    sne_v_byte(vx, byte) {
        let jump = this.v_registers[vx] !== byte;
        this.increment_program_counter(jump ? 2 : 1);
    }

    se_v_v(vx, vy) {
        let jump = this.v_registers[vx] === this.v_registers[vy];
        this.increment_program_counter(jump ? 2 : 1);
    }

    ld_v_byte(vx, byte) {
        this.v_registers[vx] = byte;
        this.increment_program_counter();
    }

    add_v_byte(vx, byte) {
        this.v_registers[vx] = (this.v_registers[vx] + byte) % Emulator.MOD_8_BIT;
        this.increment_program_counter()
    }

    increment_program_counter( n=1) {
        this.program_counter += n * 2;
    }


}
Emulator.MOD_4_BIT = 0x10;
Emulator.MOD_8_BIT = 0x100;
Emulator.MOD_12_BIT = 0x1000;
Emulator.FONT_DATA = [
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

module.exports = Emulator;