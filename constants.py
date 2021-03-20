from tkinter import Tk

root = Tk()

# game settings
DISPLAY_W = root.winfo_screenwidth()
DISPLAY_H = root.winfo_screenheight()
FPS = 45


# game
CELL_SIZE = 32  # todo: домножить на размерности при переводе в пиксели
MAP_W = 1050
MAP_H = 600
INNER_SQUARE_SIZE = 256

# player


# colors

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
