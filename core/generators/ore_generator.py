# import numpy as np
# from math import sqrt
from matplotlib import pyplot as plt
#
# from trees_generator import perlin
#
#
# def perlin(x, y, seed=0):
#     np.random.seed(seed)
#     p = np.arange(256, dtype=int)
#     np.random.shuffle(p)
#     p = np.stack([p, p]).flatten()
#     xi = x.astype(int)
#     yi = y.astype(int)
#     xf = x - xi
#     yf = y - yi
#     u = fade(xf)
#     v = fade(yf)
#     n00 = gradient(p[p[xi] + yi], xf, yf)
#     n01 = gradient(p[p[xi] + yi + 1], xf, yf - 1)
#     n11 = gradient(p[p[xi + 1] + yi + 1], xf - 1, yf - 1)
#     n10 = gradient(p[p[xi + 1] + yi], xf - 1, yf)
#     x1 = linear_interpolation(n00, n10, u)
#     x2 = linear_interpolation(n01, n11, u)
#     return linear_interpolation(x1, x2, v)
#
#
# def linear_interpolation(a, b, x):
#     return a + x * (b - a)
#
#
# def fade(t):
#     return 6 * t ** 5 - 15 * t ** 4 + 10 * t ** 3
#
#
# def gradient(h, x, y):
#     vectors = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])
#     g = vectors[h % 4]
#     return g[:, :, 0] * x + g[:, :, 1] * y
#
#
# def generate_trees_locations():
#     lin_x = np.linspace(0, 5, 256, endpoint=False)
#     lin_y = np.linspace(0, 5, 256, endpoint=False)
#
#     x, y = np.meshgrid(lin_x, lin_y)
#     noise = perlin(x, y, seed=np.random.randint(1, 256))
#
#     # trees_map = np.zeros((len(noise), len(noise[0])))
#
#     normalized_noise = - (noise / np.linalg.norm(noise) * 100) * 5
#     normalized_noise = np.where(normalized_noise > 1, 1, normalized_noise)
#     normalized_noise = np.where(normalized_noise < -1, -1, normalized_noise)
#
#     normalized_noise = np.where(normalized_noise > 0, np.zeros_like(normalized_noise), normalized_noise)
#     nonlinear_noise = (np.tanh(-2 * np.power(normalized_noise, 3) - 1) + 1) / 24
#
#     return nonlinear_noise
#
#
# from random import randint
#
# res = [[100] * 32] * 32
#
#
# def dist(x, y):
#     return sqrt((x - 16) ** 2 + (y - 16) ** 2)
#
#
# for y in range(32):
#     for x in range(32):
#         res[y][x] -= 0.1*dist(x, y)
#         # if abs(dist(x, y) - 5) < 1:
#         #     res[y][x] = 10
#
#
#
#
# # noise = np.where(noise < 0, 0, noise)
# plt.imshow(res)
# # plt.imshow(noise)
# #
# plt.show()
#
# def gen_ore_matrix(ore_size):
#     return np.ones((ore_size, ore_size))
import numpy as np
from constants import *
from PIL import Image
from random_generator import random_with_blocked_values
from random import randint


def gen_ore_matrix(size):
    return np.ones((size, size))


if __name__ == '__main__':

    MAP_H = 32
    MAP_W = 32
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
        neighbors = [possib_map[a][b] for a in range(i - 1, i + 2) for b in range(j - 1, j + 2) if (a, b) != (i, j)]
        num_ok_neighbors = 0
        for n in neighbors:
            if n > 0:
                num_ok_neighbors += 1

        if num_ok_neighbors == 0:
            possib_map[i][j] = np.random.randint(900, 1000)
        elif 1 <= num_ok_neighbors <= 2:
            possib_map[i][j] = np.random.randint(950, 1000)
        elif 3 <= num_ok_neighbors <= 4:
            possib_map[i][j] = np.random.randint(850, 950)
        else:
            possib_map[i][j] = np.random.randint(100, 250)

    for y in range(1, MAP_H - 1):
        for x in range(1, MAP_W - 1):
            trees_map[y][x] = int(randint(0, 1000) < possib_map[y][x])

    plt.imshow(trees_map, cmap='gray')
    plt.show()
