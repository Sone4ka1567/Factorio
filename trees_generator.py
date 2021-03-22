import numpy as np
from constants import *
from PIL import Image
from random_generator import random_with_blocked_values
from random import randint

MAP_H = 256
MAP_W = 256
possib_map = np.zeros((MAP_H, MAP_W), dtype=np.int)
trees_map = np.zeros_like(possib_map)

blocked = []

while len(blocked) < (MAP_H - 1) * (MAP_W - 1) - 5:
    # print(f'blocked_x: {blocked_x}')
    # print(f'blocked_y: {blocked_y}')
    # i = random_with_blocked_values(1, MAP_H - 2)
    # # if not i:
    # #     continue
    # j = random_with_blocked_values(1, MAP_W - 2)
    i = randint(2, MAP_H - 3)
    j = randint(2, MAP_W - 3)
    # while (i, j) in blocked:
    #     print(i, j)
    #     i = randint(1, MAP_H - 2)
    #     j = randint(1, MAP_W - 2)
    blocked.append((i, j))

    # if not j:
    #     continue
    neighbors = [possib_map[a][b] for a in range(i - 2, i + 3) for b in range(j - 2, j + 3) if (a, b) != (i, j)]
    num_ok_neighbors = 0
    for n in neighbors:
        if n > 0:
            num_ok_neighbors += 1

    if num_ok_neighbors == 0:
        possib_map[i][j] = np.random.randint(0, 10)
    elif 1 <= num_ok_neighbors <= 3:
        possib_map[i][j] = np.random.randint(500, 800)
    elif 3 <= num_ok_neighbors <= 5:
        possib_map[i][j] = np.random.randint(400, 600)
    elif 5 <= num_ok_neighbors <= 8:
        possib_map[i][j] = np.random.randint(100, 200)
    elif 8 <= num_ok_neighbors <= 12:
        possib_map[i][j] = np.random.randint(50, 100)
    else:
        possib_map[i][j] = np.random.randint(0, 5)

for y in range(1, MAP_H - 1):
    for x in range(1, MAP_W - 1):
        trees_map[y][x] = int(randint(0, 1000) < possib_map[y][x])

Image.fromarray(trees_map * 50).show()
