import random
from math import sin, cos, sqrt
import numpy as np
from ken_perlin_noise import gen_perlin_noise
import constants as const
from random_generator import random_point_with_blocked_square
from core.virtual_objects.raw_materials.raw_materials import (
    IronBatch,
    CopperBatch,
    StoneBatch,
    CoalBatch,
    WaterBatch,
)


def normalize(matrix: np.array):
    min_el = np.min(matrix)
    max_el = np.max(matrix)
    return (matrix - min_el) / (max_el - min_el)


class OresGenerator:
    """
    generates bounds of ores && water
    """

    def __init__(
        self, radius_coefficient_bounds, ore_size, num_ores, map_width, map_height
    ):
        self.radius_coefficient_bounds = radius_coefficient_bounds
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
            self._mtx_coordinates(*inner_square_bounds[0]),
            self._mtx_coordinates(*inner_square_bounds[1]),
        )
        basic_square_size_half = 128  # CONST coef
        basic_square_bounds = (
            (-basic_square_size_half, -basic_square_size_half),
            (basic_square_size_half, basic_square_size_half),
        )
        self.basic_square_mtx_bounds = (
            self._mtx_coordinates(*basic_square_bounds[0]),
            self._mtx_coordinates(*basic_square_bounds[1]),
        )
        self.ores_with_types = self._generate_ores_bounds()

    @staticmethod
    def _mtx_coordinates(x, y):
        return x + const.MAP_W // 2, y + const.MAP_H // 2

    @staticmethod
    def _dist(point1: tuple, point2: tuple) -> float:
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
        perlin_noise = normalize(gen_perlin_noise(size, size))

        raw_radial_gradient = np.fromfunction(
            lambda x, y: np.sqrt((x - size // 2) ** 2 + (y - size // 2) ** 2),
            shape=(size, size),
        )
        radial_gradient = normalize(1 - raw_radial_gradient)

        n = 0.24
        res = n * perlin_noise - radial_gradient * (1 - n)
        res = normalize(res)
        res = np.where(res < 0.7, res, 1)
        res = (1 - res) * 1000
        res = np.where(res > 500, res ** 2 / 1000, res ** 3 / 500000)
        return res

    def _gen_circle_rad(self, diagonal) -> int:
        return int(random.uniform(*self.radius_coefficient_bounds) * diagonal)

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
        while self._dist(fourth_ore_center, third_ore_center) <= int(
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
            fifth_ore_center,
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
        for _ in range(self.num_ores - 4):
            x, y = random_point_with_blocked_square(
                self.ore_size,
                self.ore_size,
                self.map_width - self.ore_size,
                self.map_height - self.ore_size,
                blocked_square,
            )
            for gen_ore_center in outer_ores_centers:
                while self._dist((x, y), gen_ore_center) <= int(outer_ore_diagonal * 4):
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

        for i, _ in enumerate(ores_with_types):
            ores_with_types[i].append(self.gen_ore_matrix(self.ore_size))

        return ores_with_types

    def create_batch_for_cell(self, x, y):
        for bounds, batch_type, ore_matrix in self.ores_with_types:
            if self._point_on_ore(x, y, bounds):
                return batch_type(ore_matrix[x - bounds[0][0]][y - bounds[0][1]])
            return None


# if __name__ == "__main__":
#
#     MAP_H = 32
#     MAP_W = 32
#     possib_map = np.zeros((MAP_H, MAP_W), dtype=np.int)
#
#     blocked = []
#
#     while len(blocked) < (MAP_H - 1) * (MAP_W - 1) - 5:
#         # print(f'blocked_x: {blocked_x}')
#         # print(f'blocked_y: {blocked_y}')
#         # i = random_with_blocked_values(1, MAP_H - 2)
#         # # if not i:
#         # #     continue
#         # j = random_with_blocked_values(1, MAP_W - 2)
#         i = randint(2, MAP_H - 3)
#         j = randint(2, MAP_W - 3)
#         # while (i, j) in blocked:
#         #     print(i, j)
#         #     i = randint(1, MAP_H - 2)
#         #     j = randint(1, MAP_W - 2)
#         blocked.append((i, j))
#
#         # if not j:
#         #     continue
#         neighbors = [
#             possib_map[a][b]
#             for a in range(i - 1, i + 2)
#             for b in range(j - 1, j + 2)
#             if (a, b) != (i, j)
#         ]
#         num_ok_neighbors = 0
#         for n in neighbors:
#             if n > 0:
#                 num_ok_neighbors += 1
#
#         if num_ok_neighbors == 0:
#             possib_map[i][j] = np.random.randint(900, 1000)
#         elif 1 <= num_ok_neighbors <= 2:
#             possib_map[i][j] = np.random.randint(950, 1000)
#         elif 3 <= num_ok_neighbors <= 4:
#             possib_map[i][j] = np.random.randint(850, 950)
#         else:
#             possib_map[i][j] = np.random.randint(100, 250)
#
#
#     trees_map =
#     for y in range(1, MAP_H - 1):
#         for x in range(1, MAP_W - 1):
#             trees_map[y][x] = int(randint(0, 1000) < possib_map[y][x])
#
#     plt.imshow(trees_map, cmap="gray")
#     plt.show()
