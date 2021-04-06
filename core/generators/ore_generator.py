from random_generator import random_point_with_blocked_square
from matplotlib import pyplot as plt
from core.virtual_objects.raw_materials.raw_materials import (
    IronBatch,
    CopperBatch,
    StoneBatch,
    CoalBatch,
    WaterBatch
)

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
# def self.dist(x, y):
#     return sqrt((x - 16) ** 2 + (y - 16) ** 2)
#
#
# for y in range(32):
#     for x in range(32):
#         res[y][x] -= 0.1*self.dist(x, y)
#         # if abs(self.dist(x, y) - 5) < 1:
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
from random import randint
import random
from math import sin, cos, sqrt
import constants as const


class OresGenerator:
    """
    generates bounds of ores && water
    """

    def __init__(self, radius_coef_bounds, ore_size, num_ores, map_width, map_height):
        self.radius_coef_bounds = radius_coef_bounds
        self.ore_size = ore_size
        self.num_ores = num_ores
        self.map_width = map_width
        self.map_height = map_height

        self.ore_size_half = self.ore_size // 2
        inner_square_size = self.ore_size * 2  # CONST coef
        inner_square_size_half = inner_square_size // 2
        inner_square_bounds = (
            (-inner_square_size_half, -inner_square_size_half),
            (inner_square_size_half, inner_square_size_half),
        )
        self.inner_square_mtx_bounds = (
            self.mtx_coordinates(*inner_square_bounds[0]),
            self.mtx_coordinates(*inner_square_bounds[1]),
        )
        basic_square_size_half = 128  # CONST coef
        basic_square_bounds = (
            (-basic_square_size_half, -basic_square_size_half),
            (basic_square_size_half, basic_square_size_half),
        )
        self.basic_square_mtx_bounds = (
            self.mtx_coordinates(*basic_square_bounds[0]),
            self.mtx_coordinates(*basic_square_bounds[1]),
        )
        self.ores_with_types = self._generate_ores_bounds()

    @staticmethod
    def mtx_coordinates(x, y):
        return x + const.MAP_W // 2, y + const.MAP_H // 2

    @staticmethod
    def dist(point1: tuple, point2: tuple) -> float:
        return sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

    @staticmethod
    def _point_on_ore(x, y, ore):
        return ore[0][0] < x < ore[1][0] and ore[0][1] < y < ore[1][1]

    @staticmethod
    def _get_ore_center(prev_ore_center, distance):
        degree = random.randint(0, 360)
        center = (
            int(prev_ore_center[0] + sin(degree) * distance),
            int(prev_ore_center[1] + cos(degree) * distance),
        )
        crossing = (
            int(prev_ore_center[0] + sin(degree) * distance / 2),
            int(prev_ore_center[1] + cos(degree) * distance / 2),
        )
        return center, crossing

    @staticmethod
    def gen_ore_matrix(size):
        return np.ones((size, size))

    def _gen_circle_rad(self, diagonal) -> int:
        return int(random.uniform(*self.radius_coef_bounds) * diagonal)

    def _gen_inner_ores_centers(self):
        first_ore_center = (
            random.randint(
                self.inner_square_mtx_bounds[0][0] + self.ore_size_half,
                self.inner_square_mtx_bounds[1][0] - self.ore_size_half,
            ),
            random.randint(
                self.inner_square_mtx_bounds[0][1] + self.ore_size_half,
                self.inner_square_mtx_bounds[1][1] - self.ore_size_half,
            ),
        )
        inner_ore_diagonal = self.ore_size * sqrt(2)

        inner_ore_radius = self._gen_circle_rad(diagonal=inner_ore_diagonal)
        second_ore_center, first_crossing = self._get_ore_center(
            first_ore_center, inner_ore_radius * 2
        )
        third_ore_center = self._get_ore_center(
            first_crossing, int(inner_ore_radius * 2)
        )[0]
        fourth_ore_center = self._get_ore_center(
            first_crossing, int(inner_ore_radius * 2)
        )[0]
        fifth_ore_center = self._get_ore_center(
            first_crossing, int(inner_ore_radius * 3)
        )[0]
        while self.dist(fourth_ore_center, third_ore_center) <= int(
                inner_ore_radius * 2
        ):
            fourth_ore_center = self._get_ore_center(
                first_crossing, int(inner_ore_radius * 2)
            )[0]

            fifth_ore_center = self._get_ore_center(
                first_crossing, int(inner_ore_radius * 3)
            )[0]

        ores_centers = [
            first_ore_center,
            second_ore_center,
            third_ore_center,
            fourth_ore_center,
            fifth_ore_center
        ]
        return ores_centers

    def _gen_ore_centers(self):
        inner_ores_centers = self._gen_inner_ores_centers()

        outer_ore_diagonal = self.ore_size * sqrt(2)

        blocked_square = (
            [
                self.basic_square_mtx_bounds[0][0] - self.ore_size,
                self.basic_square_mtx_bounds[0][1] - self.ore_size,
            ],
            [
                self.basic_square_mtx_bounds[1][0] + self.ore_size,
                self.basic_square_mtx_bounds[1][1] + self.ore_size,
            ],
        )
        outer_ores_centers = []
        for ore in range(self.num_ores - 4):
            x, y = random_point_with_blocked_square(
                self.ore_size,
                self.ore_size,
                self.map_width - self.ore_size,
                self.map_height - self.ore_size,
                blocked_square,
            )
            for gen_ore_center in outer_ores_centers:
                while self.dist((x, y), gen_ore_center) <= int(outer_ore_diagonal * 4):
                    x, y = random_point_with_blocked_square(
                        self.ore_size,
                        self.ore_size,
                        self.map_width - self.ore_size,
                        self.map_height - self.ore_size,
                        blocked_square,
                    )
            outer_ores_centers.append((x, y))

        inner_ores_bounds = []
        for ore_center in inner_ores_centers:
            inner_ores_bounds.append(
                [
                    [
                        ore_center[0] - self.ore_size_half,
                        ore_center[1] - self.ore_size_half,
                    ],
                    [
                        ore_center[0] + self.ore_size_half,
                        ore_center[1] + self.ore_size_half,
                    ],
                ]
            )

        outer_ores_bounds = []
        for ore_center in outer_ores_centers:
            outer_ores_bounds.append(
                [
                    [
                        ore_center[0] - self.ore_size_half,
                        ore_center[1] - self.ore_size_half,
                    ],
                    [
                        ore_center[0] + self.ore_size_half,
                        ore_center[1] + self.ore_size_half,
                    ],
                ]
            )
        return inner_ores_bounds, outer_ores_bounds

    def _generate_ores_bounds(self):

        inner_ores_bounds, outer_ores_bounds = self._gen_ore_centers()

        batch_types = [IronBatch, CoalBatch, CopperBatch, StoneBatch, WaterBatch]
        random.shuffle(batch_types)

        ores_with_types = []
        for idx, ore_bounds in enumerate(inner_ores_bounds):
            ores_with_types.append([ore_bounds, batch_types[idx]])

        for ore_bounds in outer_ores_bounds:
            ores_with_types.append([ore_bounds, random.choice(batch_types)])

        for i in range(len(ores_with_types)):
            ores_with_types[i].append(self.gen_ore_matrix(self.ore_size))

        return ores_with_types

    def create_batch_for_cell(self, x, y):
        for bounds, batch_type, ore_matrix in self.ores_with_types:
            if self._point_on_ore(x, y, bounds):
                return batch_type(ore_matrix[x - bounds[0][0]][y - bounds[0][1]])


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
