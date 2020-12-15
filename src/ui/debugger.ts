class Debugger {

    private readonly emulator: Emulator;
    private readonly vFields: HTMLInputElement[] = [];
    private readonly iField: HTMLInputElement;
    private readonly dtField: HTMLInputElement;
    private readonly stField: HTMLInputElement;
    private readonly spField: HTMLInputElement;
    private readonly pcField: HTMLInputElement;
    private readonly opField: HTMLInputElement;
    private readonly speedField: HTMLInputElement;

    constructor(parent: HTMLElement, emulator: Emulator) {
        this.emulator = emulator;
        let table = document.createElement('table');
        parent.appendChild(table);

        this.createRegisters(table);  // Fills left and middle columns
        this.iField = this.createIField(table);
        this.dtField = this.createDTField(table);
        this.stField = this.createSTField(table);
        this.spField = this.createSPField(table);
        this.pcField = this.createPCField(table);
        this.opField = Debugger.createOPField(table);
        this.createStackButton(table);
        this.createMemoryButton(table);
        this.speedField = this.createSpeedField(parent);

        this.updateFields();
    }

    private createRegisters(table: HTMLTableElement): void {
        for (let i = 0; i < Emulator.V_REGISTER_COUNT; i++) {
            let name = 'V' + i.toString(16);
            let [label, field] = Debugger.createRegisterField(name, 0xFF, (value: number) => {
                this.emulator.vRegisters[i] = value;
            });
            let div = document.createElement('div');
            div.appendChild(label);
            div.appendChild(field);
            Debugger.setCell(div, table, i % 8, Math.floor(i / 8));
            this.vFields.push(field);
        }
    }

    private createIField(table: HTMLTableElement): HTMLInputElement {
        let [label, field] = Debugger.createRegisterField('I ', 0xFFFF, (value: number) => {
            this.emulator.iRegister = value;
        });
        let div = document.createElement('div');
        div.appendChild(label);
        div.appendChild(field);
        Debugger.setCell(div, table, 0, 2);
        return field;
    }

    private createDTField(table: HTMLTableElement): HTMLInputElement {
        let [label, field] = Debugger.createRegisterField('DT', 0xFF, (value: number) => {
            this.emulator.dtRegister = value;
        });
        let div = document.createElement('div');
        div.appendChild(label);
        div.appendChild(field);
        Debugger.setCell(div, table, 1, 2);
        return field;
    }

    private createSTField(table: HTMLTableElement): HTMLInputElement {
        let [label, field] = Debugger.createRegisterField('ST', 0xFF, (value: number) => {
            this.emulator.stRegister = value;
        });
        let div = document.createElement('div');
        div.appendChild(label);
        div.appendChild(field);
        Debugger.setCell(div, table, 2, 2);
        return field;
    }

    private createSPField(table: HTMLTableElement): HTMLInputElement {
        let [label, field] = Debugger.createRegisterField('SP', 0xFF, (value: number) => {
            this.emulator.stackPointer = value;
        });
        let div = document.createElement('div');
        div.appendChild(label);
        div.appendChild(field);
        Debugger.setCell(div, table, 3, 2);
        return field;
    }

    private createPCField(table: HTMLTableElement): HTMLInputElement {
        let [label, field] = Debugger.createRegisterField('PC', 0xFFFF, (value: number) => {
            this.emulator.programCounter = value;
        });
        let div = document.createElement('div');
        div.appendChild(label);
        div.appendChild(field);
        Debugger.setCell(div, table, 4, 2);
        return field;
    }

    private static createOPField(table: HTMLTableElement): HTMLInputElement {
        let [label, field] = Debugger.createRegisterField('OP', 0xFFFF, (v: number) => {});
        field.readOnly = true;
        let div = document.createElement('div');
        div.appendChild(label);
        div.appendChild(field);
        Debugger.setCell(div, table, 5, 2);
        return field;
    }

    private createStackButton(table: HTMLTableElement): void {
        let btn = document.createElement('button');
        btn.innerText = 'Stack';
        btn.classList.add('debuggerStackButton');
        Debugger.setCell(btn, table, 6, 2);
    }

    private createMemoryButton(table: HTMLTableElement): void {
        let btn = document.createElement('button');
        btn.innerText = 'Memory';
        btn.classList.add('debuggerMemoryButton');
        Debugger.setCell(btn, table, 7, 2);
    }

    private createSpeedField(parent: HTMLElement): HTMLInputElement {
        let label = document.createElement('label');
        let field = document.createElement('input');
        field.id = "DebuggerSpeedSlider";
        field.type = 'number';
        field.min = '1';
        field.max = '2000';
        field.value = '1';
        label.htmlFor = field.id;
        label.textContent = 'Speed (ms)';
        let div = document.createElement('div');
        div.appendChild(label);
        div.appendChild(field);
        parent.appendChild(div);
        return field;
    }

    private updateFields() {
        for (let i = 0; i < this.vFields.length; i++) {
            this.vFields[i].value = this.emulator.vRegisters[i].toString(16);
        }
        this.iField.value = this.emulator.iRegister.toString(16);
        this.dtField.value = this.emulator.dtRegister.toString(16);
        this.stField.value = this.emulator.stRegister.toString(16);
        this.spField.value = this.emulator.stackPointer.toString(16);
        this.pcField.value = this.emulator.programCounter.toString(16);
    }

    private static createRegisterField(name: string, maxValue: number, onSet: Function): [HTMLSpanElement, HTMLInputElement] {
        let label = document.createElement('span');
        label.innerText = name;
        label.classList.add('debuggerRegisterLabel');
        let field = document.createElement('input');
        field.value = '0';
        field.pattern = '(0x|0)?[0-9a-f]+';
        field.classList.add('debuggerRegisterField');

        field.onkeydown = (e) => {
            if (e.key === 'Enter') {
                let value = field.valueAsNumber;
                if (value < 0 || value >= maxValue) {
                    onSet(field.valueAsNumber);
                }
            }
        };
        field.onblur = () => onSet(field.valueAsNumber);

        return [label, field];
    }

    private static setCell(element: HTMLElement, table: HTMLTableElement, row: number, col: number): void {
        // Expand table vertically if needed
        for (let i = table.childNodes.length; i <= row; i++) {
            table.appendChild(document.createElement('tr'));
        }
        let desiredRow = table.childNodes[row];
        // Expand table horizontally if needed
        for (let i = desiredRow.childNodes.length; i <= col; i++) {
            desiredRow.appendChild(document.createElement('td'));
        }
        desiredRow.childNodes[col].appendChild(element);
    }
}