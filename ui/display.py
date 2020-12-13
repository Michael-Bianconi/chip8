import tkinter as tk
from typing import List


class Display(tk.Canvas):
    """
    Canvas-object for pixel drawing.
    """

    PIXEL_COLOR = 'white'
    BG_COLOR = 'black'

    def __init__(self, canvas_size: tuple, pixel_size: tuple, window: tk.Tk):
        super().__init__(window, width=canvas_size[0], height=canvas_size[1], bg=Display.BG_COLOR)
        self.pixel_width, self.pixel_height = pixel_size

    def set_pixels(self, pixels: List[tuple]) -> None:
        for pixel in pixels:
            self.set_pixel(*pixel)

    def set_pixel(self, x: bool, y: bool, state: bool) -> None:
        upper_left = x * self.pixel_width, y * self.pixel_height
        bottom_right = upper_left[0] + self.pixel_width, upper_left[1] + self.pixel_height
        fill = Display.PIXEL_COLOR if state else Display.BG_COLOR
        super().create_rectangle(*upper_left, *bottom_right, fill=fill)
