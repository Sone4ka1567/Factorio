from abc import ABC, abstractmethod
import constants as const
import numpy as np
from PIL import Image
from math import sin, cos, sqrt
from copy import copy
import random
from random_generator import random_point_with_blocked_square
from core.generators.trees_generator import gen_trees_map
from core.generators.surface_generator import gen_surface_noise
from matplotlib import pyplot as plt
from core.generators.ore_generator import gen_ore_matrix
from core.virtual_objects.raw_materials.raw_materials import (
    IronBatch,
    CopperBatch,
    StoneBatch,
    CoalBatch,
    TreeBatch,
)


def mtx_coordinates(x, y):
    return x + const.MAP_W // 2, y + const.MAP_H // 2


def dist(point1: tuple, point2: tuple) -> float:
    return sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


class MapCell:
    def __init__(self, category: str):
        self.category: str = category
        self.usable_object = None
        self.raw_material_batch = None

    def __str__(self):
        return f"{self.category}, {type(self.raw_material_batch)}"


class Map(ABC):
    height = const.MAP_H
    width = const.MAP_W
    num_ores = int
    ore_size: int
    radius_coef_bounds: tuple
    def __init__(self):
        self.map_matrix = [[None for j in range(self.width)] for i in range(self.height)]

    @staticmethod
    def point_on_ore(x, y, ore):
        return ore[0][0] < x < ore[1][0] and ore[0][1] < y < ore[1][1]

    @staticmethod
    def get_ore_center(prev_ore_center, distance):
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

    def generate_matrix(self):
        ore_size_half = self.ore_size // 2
        inner_square_size = self.ore_size * 2  # CONST coef
        inner_square_size_half = inner_square_size // 2
        inner_square_bounds = (
            (-inner_square_size_half, -inner_square_size_half),
            (inner_square_size_half, inner_square_size_half),
        )
        inner_square_mtx_bounds = (
            mtx_coordinates(*inner_square_bounds[0]),
            mtx_coordinates(*inner_square_bounds[1]),
        )
        basic_square_size_half = 128  # CONST coef
        basic_square_bounds = (
            (-basic_square_size_half, -basic_square_size_half),
            (basic_square_size_half, basic_square_size_half),
        )
        basic_square_mtx_bounds = (
            mtx_coordinates(*basic_square_bounds[0]),
            mtx_coordinates(*basic_square_bounds[1]),
        )

        def gen_circle_rad(diagonal) -> int:
            return int(random.uniform(*self.radius_coef_bounds) * diagonal)

        def gen_inner_ores_centers():
            first_ore_center = (
                random.randint(
                    inner_square_mtx_bounds[0][0] + ore_size_half,
                    inner_square_mtx_bounds[1][0] - ore_size_half,
                ),
                random.randint(
                    inner_square_mtx_bounds[0][1] + ore_size_half,
                    inner_square_mtx_bounds[1][1] - ore_size_half,
                ),
            )



            inner_ore_diagonal = self.ore_size * sqrt(2)

            inner_ore_radius = gen_circle_rad(diagonal=inner_ore_diagonal)
            second_ore_center, first_crossing = self.get_ore_center(
                first_ore_center, inner_ore_radius * 2
            )
            third_ore_center = self.get_ore_center(
                first_crossing, int(inner_ore_radius * 2)
            )[0]
            fourth_ore_center = self.get_ore_center(
                first_crossing, int(inner_ore_radius * 2)
            )[0]
            while dist(fourth_ore_center, third_ore_center) <= int(
                    inner_ore_radius * 2
            ):
                fourth_ore_center = self.get_ore_center(
                    first_crossing, int(inner_ore_radius * 2)
                )[0]

            ores_centers = [
                first_ore_center,
                second_ore_center,
                third_ore_center,
                fourth_ore_center,
            ]
            print(ores_centers)
            return ores_centers

        outer_ore_size = self.ore_size

        def gen_ore_centers():
            inner_ores_centers = gen_inner_ores_centers()

            outer_ore_diagonal = outer_ore_size * sqrt(2)

            blocked_square = (
                [
                    basic_square_mtx_bounds[0][0] - outer_ore_size,
                    basic_square_mtx_bounds[0][1] - outer_ore_size,
                ],
                [
                    basic_square_mtx_bounds[1][0] + outer_ore_size,
                    basic_square_mtx_bounds[1][1] + outer_ore_size,
                ],
            )
            outer_ores_centers = []
            for ore in range(self.num_ores - 4):
                x, y = random_point_with_blocked_square(
                    outer_ore_size,
                    outer_ore_size,
                    self.width - outer_ore_size,
                    self.height - outer_ore_size,
                    blocked_square,
                )
                for gen_ore_center in outer_ores_centers:
                    while dist((x, y), gen_ore_center) <= int(outer_ore_diagonal * 4):
                        x, y = random_point_with_blocked_square(
                            outer_ore_size,
                            outer_ore_size,
                            self.width - outer_ore_size,
                            self.height - outer_ore_size,
                            blocked_square,
                        )
                outer_ores_centers.append((x, y))

            ore_size_half = self.ore_size // 2
            inner_ores_bounds = []
            for ore_center in inner_ores_centers:
                inner_ores_bounds.append(
                    [
                        [
                            ore_center[0] - ore_size_half,
                            ore_center[1] - ore_size_half,
                        ],
                        [
                            ore_center[0] + ore_size_half,
                            ore_center[1] + ore_size_half,
                        ],
                    ]
                )  # print(pic_mtx)

            ore_size_half = outer_ore_size // 2
            outer_ores_bounds = []
            for ore_center in outer_ores_centers:
                outer_ores_bounds.append(
                    [
                        [
                            ore_center[0] - ore_size_half,
                            ore_center[1] - ore_size_half,
                        ],
                        [
                            ore_center[0] + ore_size_half,
                            ore_center[1] + ore_size_half,
                        ],
                    ]
                )  # print(pic_mtx)
            return inner_ores_bounds, outer_ores_bounds

        inner_ores_bounds, outer_ores_bounds = gen_ore_centers()

        matrix = np.array([[0] * self.width] * self.height)
        print(outer_ores_bounds)

        batch_types = [IronBatch, CoalBatch, CopperBatch, StoneBatch]
        random.shuffle(batch_types)

        ores_with_types = []
        for idx, ore_bounds in enumerate(inner_ores_bounds):
            ores_with_types.append([ore_bounds, batch_types[idx]])

        for ore_bounds in outer_ores_bounds:
            ores_with_types.append([ore_bounds, random.choice(batch_types)])

        # TODO:
        """
        * gen_ore_matrix() - implement algo
        * test all
        """

        trees_matrix = gen_trees_map(self.height, self.width)

        for i in range(len(ores_with_types)):
            ores_with_types[i].append(gen_ore_matrix(self.ore_size))

        def create_batch_for_cell(x, y):
            for bounds, batch_type, ore_matrix in ores_with_types:
                if self.point_on_ore(x, y, bounds):
                    return batch_type(ore_matrix[x - bounds[0][0]][y - bounds[0][1]])

        surface_noise = gen_surface_noise(self.height, self.width)
        plt.imshow(surface_noise)
        plt.show()

        def interpret_surface_noise(el):
            if el == 1:
                return "dark"
            if el == 2:
                return "water"
            if el == 3:
                return "light"

        for y in range(self.height):
            for x in range(self.width):
                cell = MapCell(interpret_surface_noise(surface_noise[y][x]))
                # фабричны метод (зачем....)
                # raw_material_gen, amount = get_ore_of_cell(x, y)
                # if raw_material_gen:
                #     cell.raw_material_batch = raw_material_gen.generate_raw_material(amount)
                if cell.category != "water":
                    if trees_matrix[y][x]:
                        cell.raw_material_batch = TreeBatch(random.randint(10, 20))  # CONST
                    else:
                        cell.raw_material_batch = create_batch_for_cell(x, y)
                self.map_matrix[y][x] = cell
        # print(self.map_matrix[10:][10:])

        categories = {'water': 7, 'dark': 8, 'light': 9}
        map_objects = {'IronBatch': 1, 'CopperBatch': 2, 'CoalBatch': 3, 'StoneBatch': 4, 'TreeBatch': 5}
        res = np.zeros((self.height, self.width))
        for y in range(self.height):
            for x in range(self.width):
                cell: MapCell = self.map_matrix[y][x]
                # print(cell)
                res[y][x] = categories[cell.category]
                if cell and cell.raw_material_batch:
                    res[y][x] = map_objects[cell.raw_material_batch.__name__()]

            #     print(b.category, end=' ')
            # print()
        plt.imshow(res)
        plt.show()


class EasyMap(Map):
    def __init__(self):
        super().__init__()
        self.ore_size = 32
        self.radius_coef_bounds = (0.8, 1)
        self.num_ores = 12


class HardMap(Map):
    def __init__(self):
        super().__init__()
        self.ore_size = 28
        self.radius_coef_bounds = (1, 1.2)
        self.num_ores = 10


class MapCreator:
    @abstractmethod
    def create_map(self):
        """
        factory method implementation
        :return: Map object
        """
        pass

    def gen_map(self):
        map_object: Map = self.create_map()
        map_object.generate_matrix()
        return map_object


class EasyMapCreator(MapCreator):
    def create_map(self):
        return EasyMap()


class HardMapCreator(MapCreator):
    def create_map(self):
        return HardMap()


if __name__ == "__main__":
    creator = EasyMapCreator()
    creator.gen_map()
#

#
#
# def noise_to_kind():
#     pass
#
#
#
#
# def get_ore_of_cell(x, y):
#     pass
#
#
# for y in range(len(const.MAP_H)):
#     for x in range(const.MAP_W):
#         cell = MapCell(interpret_surface_noise(surface_noise[y][x]))
#         # фабричны метод (зачем....)
#         # raw_material_gen, amount = get_ore_of_cell(x, y)
#         # if raw_material_gen:
#         #     cell.raw_material_batch = raw_material_gen.generate_raw_material(amount)
#
#         cell.raw_material_batch = create_batch_for_cell(x, y)
#         map[y][x] = cell
#
#
# def create_batch_for_cell(x, y):
