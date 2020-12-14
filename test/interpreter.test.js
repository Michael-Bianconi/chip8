const Emulator = require('../build/js/emulator');
const Interpreter = require('../build/js/interpreter');

test('BREAKPOINT', () => {
   let emulator = new Emulator();
   let interpreter = new Interpreter(emulator);
   interpreter.interpret('BREAKPOINT 0x504');
   expect(emulator.breakpoints.includes(0x504)).toBeTruthy();
   interpreter.interpret('BREAKPOINT 0xFFF');
   expect(emulator.breakpoints.includes(0xFFF)).toBeTruthy();
   interpreter.interpret('   BrEaKpoInT   10  ');
   expect(emulator.breakpoints.includes(10)).toBeTruthy();

   // Truthy means we had an error
   expect(interpreter.interpret( 'BREAKPOINT')).toBeTruthy();
   expect(interpreter.interpret( 'breakpoint 0xfdk')).toBeTruthy();
   expect(interpreter.interpret('breakpoint 0x1000')).toBeTruthy();
   expect(interpreter.interpret('breakpoint -5')).toBeTruthy();
});