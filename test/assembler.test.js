const Assembler = require('../build/js/assembler/assembler');

// These test lines are not preprocessed, so don't do anything too
// fancy. The Preprocessor -> Assembler pipeline is tested on the
// actual sample test files.
test('ADD I, Vx', () => {
    expect(Assembler.assembleLine('ADD I, V4')).toBe(0xF41E);
    expect(Assembler.assembleLine('ADD I, VF')).toBe(0xFF1E);
    expect(Assembler.assembleLine('ADD I, F')).toBeNull();
    expect(Assembler.assembleLine('ADD I  V6')).toBeNull();
    expect(Assembler.assembleLine('ADD I, Vx')).toBeNull();
    expect(Assembler.assembleLine('ADD I, V-4')).toBeNull();
});

test('ADD Vx, BYTE', () => {
    expect(Assembler.assembleLine('ADD V4, 0X5')).toBe(0x7405);
    expect(Assembler.assembleLine('ADD V7, 0XFA')).toBe(0x77FA);
});

test('ADD Vx, Vy', () => {
    expect(Assembler.assembleLine('ADD V4, V5')).toBe(0x8454);
    expect(Assembler.assembleLine('ADD V0, VF')).toBe(0x80F4);
});

test('DRW Vx, Vy, Nibble', () => {
    expect(Assembler.assembleLine("DRW V1, V2, 0X3")).toBe(0xD123);
    expect(Assembler.assembleLine("DRW VF, V0, 10")).toBe(0xDF0A);
});
