const Disassembler = require('../build/js/assembler/disassembler');

test('ADD', () => {
   expect(Disassembler.disassemble(0x7056)).toBe('ADD V0, 0X56');
});

test('JP', () => {
    expect(Disassembler.disassemble(0x1000)).toBe('JP 0X000');
    expect(Disassembler.disassemble(0x1FFF)).toBe('JP 0XFFF');
});

test('LD', () => {
    expect(Disassembler.disassemble(0x6005)).toBe('LD V0, 0X05');
    expect(Disassembler.disassemble(0x64FF)).toBe('LD V4, 0XFF');
    expect(Disassembler.disassemble(0xF455)).toBe('LD [I], V4');
});


test('SE', () => {
    expect(Disassembler.disassemble(0x3005)).toBe('SE V0, 0X05');
    expect(Disassembler.disassemble(0x31FF)).toBe('SE V1, 0XFF');
});

test('SNE', () => {
    expect(Disassembler.disassemble(0x4443)).toBe('SNE V4, 0X43');
});
