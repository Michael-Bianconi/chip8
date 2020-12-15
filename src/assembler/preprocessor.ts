class Preprocessor {

    private readonly labels: Record<string, string> = {};
    private programCounter: number = 0x200;

    static removeComment(line: string): string {
        return line.split(';')[0].trim();
    }

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
}

try {
    module.exports = Preprocessor;
} catch (e) {
    // Do nothing
}