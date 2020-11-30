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

## Disassembler

### Usage
```
python3 disassembler.py <source file> <destination file>
```
