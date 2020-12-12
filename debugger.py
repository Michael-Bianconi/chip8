import sys
import tkinter as tk
from graphical.display import Display
from emulator import Emulator
from disassembler import mnemonic


class InfoGrid(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        register_grid = tk.Frame(master=self)
        self.registers = {
            'v0': tk.Label(master=register_grid, width=8),
            'v1': tk.Label(master=register_grid),
            'v2': tk.Label(master=register_grid),
            'v3': tk.Label(master=register_grid),
            'v4': tk.Label(master=register_grid),
            'v5': tk.Label(master=register_grid),
            'v6': tk.Label(master=register_grid),
            'v7': tk.Label(master=register_grid),
            'v8': tk.Label(master=register_grid),
            'v9': tk.Label(master=register_grid),
            'vA': tk.Label(master=register_grid),
            'vB': tk.Label(master=register_grid),
            'vC': tk.Label(master=register_grid),
            'vD': tk.Label(master=register_grid),
            'vE': tk.Label(master=register_grid),
            'vF': tk.Label(master=register_grid),
            'I': tk.Label(master=register_grid),
            'DT': tk.Label(master=register_grid),
            'ST': tk.Label(master=register_grid),
            'PC': tk.Label(master=register_grid),
            'SP': tk.Label(master=register_grid),
            'OP': tk.Label(master=register_grid, width=16),
        }

        left_column = []
        middle_column = []
        right_column = []

        for v in range(16):
            v_name = f'v{hex(v).upper()[2:]}'
            left_column.append((tk.Label(master=register_grid, text=v_name), self.registers[v_name]))

        right_column.append((tk.Label(master=register_grid, text='I'), self.registers['I']))
        right_column.append((tk.Label(master=register_grid, text='DT'), self.registers['DT']))
        right_column.append((tk.Label(master=register_grid, text='ST'), self.registers['ST']))
        right_column.append((tk.Label(master=register_grid, text='PC'), self.registers['PC']))
        right_column.append((tk.Label(master=register_grid, text='SP'), self.registers['SP']))
        right_column.append((tk.Label(master=register_grid, text='OP'), self.registers['OP']))

        for row, i in enumerate(left_column):
            if i[0] is not None:
                i[0].grid(row=row, column=0)
            i[1].grid(row=row, column=1)

        for row, i in enumerate(middle_column):
            if i[0] is not None:
                i[0].grid(row=row, column=2)
            i[1].grid(row=row, column=3)

        for row, i in enumerate(right_column):
            if i[0] is not None:
                i[0].grid(row=row, column=4)
            i[1].grid(row=row, column=5)

        mem_stack = tk.Frame(master=self)
        self.stack_btn = tk.Button(master=mem_stack, text='Stack')
        self.memory_btn = tk.Button(master=mem_stack, text='Memory')
        mem_stack.pack()
        self.stack_btn.pack(side='left')
        self.memory_btn.pack(side='left')
        register_grid.pack(side='top')

        for key in self.registers.keys():
            self.set_register(key, 0)

    def set_register(self, name: str, value: int) -> None:
        self.registers[name].config(text=hex(value))

    def set_op(self, value: str) -> None:
        self.registers['OP'].config(text=value)

def play_pause_step_frame(master) -> tk.Frame:
    frame = tk.Frame(master=master)
    play_button = tk.Button(master=frame, text='>>')
    pause_button = tk.Button(master=frame, text='||')
    step_button = tk.Button(master=frame, text='|>')  # You're not my real button!
    play_button.pack(side='left')
    pause_button.pack(side='left')
    step_button.pack(side='left')
    return frame


window = tk.Tk()
window.title('Chip-8 Emulator')
display = Display((640, 320), (10, 10), window)
info_grid = InfoGrid(window)
pps = play_pause_step_frame(window)
pps.pack(side='top')
display.pack(side='left')
info_grid.pack(side='left')

with open(sys.argv[1], 'rb') as source:
    emulator = Emulator(source)

def foo():
    emulator.next()
    display.set_pixels(emulator.pixels_to_update)
    info_grid.set_register('v0', emulator.v_registers[0])
    info_grid.set_register('v1', emulator.v_registers[1])
    info_grid.set_register('v2', emulator.v_registers[2])
    info_grid.set_register('I', emulator.i_register)
    info_grid.set_register('PC', emulator.program_counter)
    opcode = int.from_bytes(emulator.memory[emulator.program_counter:emulator.program_counter + 2], 'big')
    info_grid.set_op(mnemonic(opcode))
    window.after(1, foo)

foo()
while True:
    window.update_idletasks()
    window.update()