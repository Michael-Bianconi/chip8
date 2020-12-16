class Preprocessor {

    private readonly labels: Record<string, string> = {};
    private programCounter: number = 0x200;

    run(raw: string[]): string[] {
        return this.secondPass(this.firstPass(raw));
    }

    /**
     * Build label table. Remove labels, defines, and comments.
     * Squash excessive whitespace. Make everything upper case.
     * Remove empty lines.
     */
    firstPass(raw: string[]): string[] {
        let result: string[] = [];
        for (let i = 0; i < raw.length; i++) {
            let line = raw[i].trim().toUpperCase().replace(/\s+/, ' ');
            line = this.processLabel(Preprocessor.removeComment(line));
            if (line !== '') {
                if (!this.processDefine(line)) {
                    result.push(line);
                    this.programCounter += 2;
                }
            }
        }
        return result;
    }

    secondPass(firstPassed: string[]): string[] {
        return firstPassed.map(line => this.replaceLabels(line));
    }

    /**
     * @param line Assembly without comments (all uppercase).
     * @return Returns the rest of the line after the label, or
     *         the entire line if no label exists.
     * @throws String if a label is declared twice.
     */
    processLabel(line: string): string {
        let match = line.match(/^([A-Z_][0-9A-Z_]+)\s*:(.*)/);
        if (match !== null) {
            let [label, rest] = [match[1], match[2].trim()];
            if (this.labels[label] === undefined) {
                this.labels[label] = '0X' + this.programCounter.toString(16);
                return rest;
            } else {
                throw "Label redeclaration: " + label;
            }
        }
        return line;
    }

    /**
     * @param line Assembly without labels or comments (all uppercase).
     * @returns True if the line was a 'define' line, false otherwise.
     * @throws String if a label is declared twice.
     */
    processDefine(line: string): boolean {
        let match = line.match(/^DEFINE\s+([A-Z_][A-Z0-9_]*)\s+([A-Z0-9_]+)$/);
        if (match !== null) {
            let [key, value] = [match[1], match[2]];
            if (this.labels[key] === undefined) {
                this.labels[key] = value;
                return true;
            } else {
                throw "Label redeclaration: " + key;
            }
        } else {
            return false;
        }
    }

    replaceLabels(line: string): string {
        let [opcode, operands] = Preprocessor.splitMnemonic(line);
        for (let o = 0; o < operands.length; o++) {
            if (this.labels[operands[o]] !== undefined) {
                operands[o] = this.labels[operands[o]];
            }
        }
        return (opcode + ' ' + operands.join(', ')).trim();
    }

    /**
     * @param line Uppercase, no label, no define, no comment, not empty
     * @returns [opcode, [operands]]
     */
    static splitMnemonic(line: string): [string, string[]] {
        let opEnd = line.indexOf(' ');
        if (opEnd !== -1) {
            let [opcode, operands] = [line.slice(0, opEnd).trim(), line.slice(opEnd).trim()];
            return [opcode, operands.split(/\s*,\s*/).map(o => o.trim())];
        } else {
            return [line, []];
        }
    }

    static removeComment(line: string): string {
        return line.split(';')[0].trim();
    }
}

try {
    module.exports = Preprocessor;
} catch (e) {
    // Do nothing
}