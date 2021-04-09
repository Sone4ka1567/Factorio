from tkinter import Tk

root = Tk()

# game settings
DISPLAY_W = root.winfo_screenwidth()
DISPLAY_H = root.winfo_screenheight()
FPS = 45


# game
CELL_SIZE = 32
MAP_W = 1024  # в клетках
MAP_H = 768
PIXEL_MAP_W = MAP_W * CELL_SIZE
PIXEL_MAP_H = MAP_H * CELL_SIZE
INNER_SQUARE_SIZE = 256

# player


# colors

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

BG_COLOR = BLACK
