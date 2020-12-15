const Preprocessor = require('../build/js/assembler/preprocessor');

test('REMOVE COMMENTS', () => {
   expect(Preprocessor.removeComment('ADD V0, V1 ; add')).toBe('ADD V0, V1');
   expect(Preprocessor.removeComment('ADD V0, V1')).toBe('ADD V0, V1');
   expect(Preprocessor.removeComment('ADD V0, V1 ; add ; add')).toBe('ADD V0, V1');
   expect(Preprocessor.removeComment('')).toBe('');
});

test('PROCESS LABELS', () => {
   let p = new Preprocessor();
   expect(p.processLabel('no label')).toBe('no label');
   expect(p.processLabel('MY_LABEL:')).toBe('');
   expect(p.labels['MY_LABEL']).toBe('0X200');
   p.programCounter = 0x504;
   expect(p.processLabel('_MY_OTHER_LABEL : ADD V0, V1 ')).toBe('ADD V0, V1');
   expect(p.labels['_MY_OTHER_LABEL']).toBe('0X504');
});

test('PROCESS LABELS DUPLICATES', () => {
    let p = new Preprocessor();
    expect(p.processLabel('MY_LABEL:')).toBe('');
    expect(p.labels['MY_LABEL']).toBe('0X200');
    expect(() => p.processLabel('MY_LABEL:')).toThrow();
});

test( 'PROCESS LABELS INVALID', () => {
   let p = new Preprocessor();
   expect(p.processLabel('1LABEL:')).toBe('1LABEL:');
   expect(p.processLabel('LABEL^:')).toBe('LABEL^:');
});