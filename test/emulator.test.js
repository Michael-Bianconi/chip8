const Emulator = require('../build/js/emulator');

test('SE Vx Byte', () => {
    let e = new Emulator();
    e.programCounter = 0x500;
    e.se_v_byte(4, 5);
    expect(e.programCounter).toBe(0x502);
    e.vRegisters[4] = 5;
    e.se_v_byte(4, 5);
    expect(e.programCounter).toBe(0x506);
});

test('SNE Vx Byte', () => {
   let e = new Emulator();
   e.programCounter = 0x500;
   e.sne_v_byte(4, 5);
   expect(e.programCounter).toBe(0x504);
   e.vRegisters[4] = 5;
   e.sne_v_byte(4, 5);
   expect(e.programCounter).toBe(0x506);
});

test('SE Vx Vy', () => {
    let e = new Emulator();
    e.programCounter = 0x500;
    e.vRegisters[3] = 5;
    e.se_v_v(4, 3);
    expect(e.programCounter).toBe(0x502);
    e.vRegisters[4] = 5;
    e.se_v_v(4, 3);
    expect(e.programCounter).toBe(0x506);
});

test('LD Vx Byte', () => {
    let e = new Emulator();
    e.programCounter = 0x400;
    e.vRegisters[3] = 5;
    e.ld_v_byte(3, 7);
    expect(e.vRegisters[3]).toBe(7);
    expect(e.programCounter).toBe(0x402);
});

test('ADD Vx Byte', () => {
    let e = new Emulator();
    e.programCounter = 0x400;
    e.vRegisters[4] = 0xF0;
    e.add_v_byte(4, 0xA);
    expect(e.vRegisters[4]).toBe(0xFA);
    expect(e.programCounter).toBe(0x402);
    e.add_v_byte(4, 6);
    expect(e.vRegisters[4]).toBe(0);
    expect(e.programCounter).toBe(0x404);
});

test('LD Vx Vy', () => {
    let e = new Emulator();
    e.programCounter = 0x400;
    e.vRegisters[3] = 5;
    e.vRegisters[5] = 7;
    e.ld_v_v(3, 5);
    expect(e.vRegisters[3]).toBe(7);
    expect(e.programCounter).toBe(0x402);
});

test('OR Vx Vy', () => {
    let e = new Emulator();
    e.programCounter = 0x400;
    e.vRegisters[4] = 0x84; // 10000100
    e.vRegisters[5] = 0x41; // 01000001
    e.or_v_v(4, 5);
    expect(e.vRegisters[4]).toBe(0xC5);
    expect(e.vRegisters[5]).toBe(0x41);
    expect(e.programCounter).toBe(0x402);
});

test('AND Vx Vy', () => {
    let e = new Emulator();
    e.programCounter = 0x400;
    e.vRegisters[4] = 0xC7; // 11000111
    e.vRegisters[5] = 0x51; // 01010001
    e.and_v_v(4, 5);
    expect(e.vRegisters[4]).toBe(0x41);
    expect(e.vRegisters[5]).toBe(0x51);
    expect(e.programCounter).toBe(0x402);
});

test('XOR Vx Vy', () => {
    let e = new Emulator();
    e.programCounter = 0x400;
    e.vRegisters[4] = 0xC7; // 11000111
    e.vRegisters[5] = 0x51; // 01010001
    e.xor_v_v(4, 5);
    expect(e.vRegisters[4]).toBe(0x96);
    expect(e.vRegisters[5]).toBe(0x51);
    expect(e.programCounter).toBe(0x402);
});

test('ADD Vx Vy', () => {
    let e = new Emulator();
    e.programCounter = 0x400;
    e.vRegisters[4] = 0xF0;
    e.vRegisters[5] = 0xA;
    e.add_v_v(4, 5);
    expect(e.vRegisters[4]).toBe(0xFA);
    expect(e.programCounter).toBe(0x402);
    e.add_v_v(4, 5);
    expect(e.vRegisters[4]).toBe(4);
    expect(e.programCounter).toBe(0x404);
});

test('SUB Vx Vy', () => {
    let e = new Emulator();
    e.programCounter = 0x400;
    e.vRegisters[4] = 0xF0;
    e.vRegisters[5] = 0xA;
    e.sub_v_v(4, 5);
    expect(e.vRegisters[0xF]).toBe(1);
    expect(e.vRegisters[4]).toBe(0xE6);
    expect(e.programCounter).toBe(0x402);
    e.vRegisters[5] = 0xE7;
    e.sub_v_v(4, 5);
    expect(e.vRegisters[0xF]).toBe(0);
    expect(e.vRegisters[4]).toBe(0xFF);
    expect(e.programCounter).toBe(0x404);
});

test('SHR Vx', () => {
    let e = new Emulator();
    e.programCounter = 0x400;
    e.vRegisters[4] = 0xF1;  // 11110001
    e.shr_v(4);  // 01111000
    expect(e.vRegisters[0xF]).toBe(1);
    expect(e.vRegisters[4]).toBe(0x78);
    expect(e.programCounter).toBe(0x402);
    e.shr_v(4);  // 00111100
    expect(e.vRegisters[0xF]).toBe(0);
    expect(e.vRegisters[4]).toBe(0x3C);
    expect(e.programCounter).toBe(0x404);
});

test('SUBN Vx Vy', () => {
    let e = new Emulator();
    e.programCounter = 0x400;
    e.vRegisters[4] = 0xA;
    e.vRegisters[5] = 0xF0;
    e.subn_v_v(4, 5);
    expect(e.vRegisters[0xF]).toBe(1);
    expect(e.vRegisters[4]).toBe(0xE6);
    expect(e.programCounter).toBe(0x402);
    e.vRegisters[5] = 0xE5;
    e.subn_v_v(4, 5);
    expect(e.vRegisters[0xF]).toBe(0);
    expect(e.vRegisters[4]).toBe(0xFF);
    expect(e.programCounter).toBe(0x404);
});

test('SHL Vx', () => {
    let e = new Emulator();
    e.programCounter = 0x400;
    e.vRegisters[4] = 0xB1;  // 10110001
    e.shl_v(4);  // 01100010
    expect(e.vRegisters[0xF]).toBe(1);
    expect(e.vRegisters[4]).toBe(0x62);
    expect(e.programCounter).toBe(0x402);
    e.shl_v(4);  // 11000100
    expect(e.vRegisters[0xF]).toBe(0);
    expect(e.vRegisters[4]).toBe(0xC4);
    expect(e.programCounter).toBe(0x404);
});
