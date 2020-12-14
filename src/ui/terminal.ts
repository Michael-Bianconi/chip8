class Terminal {

    private readonly userInput: HTMLInputElement;
    private readonly output: HTMLElement;

    constructor(parent: HTMLElement, onenter: (value: string) => string[]) {
        this.output = document.createElement('div');
        this.output.classList.add('terminalOutput');
        parent.appendChild(this.output);

        this.userInput = document.createElement('input');
        this.userInput.type = 'text';
        this.userInput.classList.add('terminalInput');
        this.userInput.onkeydown = ev => {
            if (ev.key === 'Enter') {
                let result = onenter(this.userInput.value);
                this.appendOutputLine(this.userInput.value);
                for (let line in result) {
                    this.appendOutputLine(line);
                }
                this.userInput.value = '';
            }
        };
        parent.appendChild(this.userInput);
    }

    appendOutputLine(value: string) {
        let line = document.createElement('span');
        line.innerText = value;
        line.classList.add('terminalOutputLine');
        this.output.append(line);
    }
}