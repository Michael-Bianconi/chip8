# Chip-8

## Assembler
## Usage
```
python3 assembler.py <source file> <destination file>
```
### Important Notes:
* All characters are case-insensitive
* All numerical values are hexadecimal
* Except for V registers, all hexadecimal values are written as `0xFF`.
* Comments start with `;`
* Labels start with a letter, are alphanumeric, and end with `:`
* Define-macros start with a letter and are alphanumeric
* There is nothing stopping you from macro-ing a keyword (e.g. `I`), but things will break
* You may declare labels and define-macros before or after using them
* You may declare labels and define-macros multiple times. Only the bottom-most declarations will be used
* You may only declare one label per line. If you want to declare multiple labels at the same place, put them on separate lines
## Disassembler

### Usage
```
python3 disassembler.py <source file> <destination file>
```

## Debugger
The debugger allows the user step through their program, as well as view and
alter registers during run-time. Commands may only be entered when the program
is paused.

#### Commands:
    RUN                           ; Start the program while it is paused
    EXIT                          ; Close the program
    BREAKPOINT <address>          ; Pause the program when PC = <address>
    REGISTERS                     ; View register contents
    SET <register> <int>          ; Set a register to the value
    STACK                         ; View the stack
    MEMORY[<address>] * <n>       ; View <n> bytes of data at memory[<address>]

