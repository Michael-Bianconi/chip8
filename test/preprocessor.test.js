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

test( 'PROCESS DEFINE', () => {
   let p = new Preprocessor();
   expect(p.processDefine('DEFINE MYDEFINE V0')).toBe(true);
   expect(p.labels['MYDEFINE']).toBe('V0');
   expect(p.processDefine('ADD V0, V1')).toBe(false);
   expect(p.processDefine('DEFINE _MYDEFINE V0')).toBe(true);
   expect(p.labels['_MYDEFINE']).toBe('V0');
   expect(p.processDefine('DEFINE')).toBe(false);
   expect(p.processDefine('DEFINE MYKEY')).toBe(false);
});

test('SPLIT MNEMONIC', () => {
   expect(Preprocessor.splitMnemonic('ADD V0, V1')).toStrictEqual(['ADD', ['V0', 'V1']]);
   expect(Preprocessor.splitMnemonic('ADD   V0  , V1')).toStrictEqual(['ADD', ['V0', 'V1']]);
   expect(Preprocessor.splitMnemonic('ADD V0,V1')).toStrictEqual(['ADD', ['V0', 'V1']]);
   expect(Preprocessor.splitMnemonic('ADD V0, V1, V2')).toStrictEqual(['ADD', ['V0', 'V1', 'V2']]);
   expect(Preprocessor.splitMnemonic('ADD V0')).toStrictEqual(['ADD', ['V0']]);
   expect(Preprocessor.splitMnemonic('ADD')).toStrictEqual(['ADD', []]);
});

test('REPLACE LABELS', () => {
   let p = new Preprocessor();
   p.processLabel('LABEL1:');
   p.processDefine('DEFINE LABEL2 VF');
   expect(p.replaceLabels('ADD LABEL1, V0')).toBe('ADD 0X200,V0');
   expect(p.replaceLabels('ADD LABEL1, LABEL2')).toBe('ADD 0X200,VF');
   expect(p.replaceLabels('ADD LABEL1')).toBe('ADD 0X200');
   expect(p.replaceLabels('ADD')).toBe('ADD');
});