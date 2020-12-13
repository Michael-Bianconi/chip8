const Emulator = require('./emulator');

test('SE Vx Byte', () => {
    let e = new Emulator();
    e.program_counter = 0x500;
    e.se_v_byte(4, 5);
    expect(e.program_counter).toBe(0x502);
    e.v_registers[4] = 5;
    e.se_v_byte(4, 5);
    expect(e.program_counter).toBe(0x506);
});

test('SNE Vx Byte', () => {
   let e = new Emulator();
   e.program_counter = 0x500;
   e.sne_v_byte(4, 5);
   expect(e.program_counter).toBe(0x504);
   e.v_registers[4] = 5;
   e.sne_v_byte(4, 5);
   expect(e.program_counter).toBe(0x506);
});

test('SE Vx Vy', () => {
    let e = new Emulator();
    e.program_counter = 0x500;
    e.v_registers[3] = 5;
    e.se_v_v(4, 3);
    expect(e.program_counter).toBe(0x502);
    e.v_registers[4] = 5;
    e.se_v_v(4, 3);
    expect(e.program_counter).toBe(0x506);
});

test('LD Vx Byte', () => {
    let e = new Emulator();
    e.program_counter = 0x400;
    e.v_registers[3] = 5;
    e.ld_v_byte(3, 7);
    expect(e.v_registers[3]).toBe(7);
    expect(e.program_counter).toBe(0x402);
});

test('ADD Vx Byte', () => {
    let e = new Emulator();
    e.program_counter = 0x400;
    e.v_registers[4] = 0xF0;
    e.add_v_byte(4, 0xA);
    expect(e.v_registers[4]).toBe(0xFA);
    expect(e.program_counter).toBe(0x402);
    e.add_v_byte(4, 6);
    expect(e.v_registers[4]).toBe(0);
    expect(e.program_counter).toBe(0x404);

});