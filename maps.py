from abc import ABC, abstractmethod
from constants import *
import numpy as np  # заблокируй себе import воздуха
from PIL import Image
from math import sin, cos, sqrt
from copy import copy
from random import randint, shuffle, choice
from random_generator import random_point_with_blocked_square
from core.generators.trees_generator import gen_trees_map
from matplotlib import pyplot as plt
from core.generators.ore_generator import gen_ore_matrix
from core.virtual_objects.raw_materials.raw_materials import IronBatch, CopperBatch, StoneBatch, CoalBatch, TreeBatch


def abs_coordinates(x, y):
    return x + MAP_W // 2, y + MAP_H // 2


def dist(point1: tuple, point2: tuple) -> float:
    return sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


class MapCell:
    def __init__(self, category):
        self.category = category
        self.usable_object = None
        self.raw_material_batch = None


class Map(ABC):
    height = MAP_H
    width = MAP_W
    map_matrix = [[None] * MAP_W] * MAP_H
    num_ores = int
    inner_square_parts: list
    ore_size: int
    radius_coef: tuple

    def generate_matrix(self):
        inner_ore_size_half = self.ore_size // 2
        inner_square_size = self.ore_size * 2  # changed
        inner_square_size_half = inner_square_size // 2
        inner_square_bounds = (
            (-inner_square_size_half, -inner_square_size_half), (inner_square_size_half, inner_square_size_half))
        print(inner_square_bounds)
        inner_square_mtx_bounds = (abs_coordinates(*inner_square_bounds[0]), abs_coordinates(*inner_square_bounds[1]))
        print('Mm', inner_square_mtx_bounds)
        basic_square_size_half = 128  # CONST
        basic_square_bounds = (
            (-basic_square_size_half, -basic_square_size_half), (basic_square_size_half, basic_square_size_half))
        basic_square_mtx_bounds = (abs_coordinates(*basic_square_bounds[0]), abs_coordinates(*basic_square_bounds[1]))
        print('b', basic_square_mtx_bounds)

        def gen_circle_rad(diagonal) -> int:
            return int((randint(*self.radius_coef) / 10) * diagonal)

        def point_on_ore(x, y, ore):
            return ore[0][0] < x < ore[1][0] and ore[0][1] < y < ore[1][1]

        def gen_inner_ores_centers():
            first_ore_center = (
                randint(inner_square_mtx_bounds[0][0] + inner_ore_size_half,
                        inner_square_mtx_bounds[1][0] - inner_ore_size_half),
                randint(inner_square_mtx_bounds[0][1] + inner_ore_size_half,
                        inner_square_mtx_bounds[1][1] - inner_ore_size_half)
            )

            def get_ore_center(prev_ore_center, distance):
                degree = randint(0, 360)
                center = (int(prev_ore_center[0] + sin(degree) * distance),
                          int(prev_ore_center[1] + cos(degree) * distance))
                crossing = (int(prev_ore_center[0] + sin(degree) * distance / 2),
                            int(prev_ore_center[1] + cos(degree) * distance / 2))
                return center, crossing

            inner_ore_diagonal = self.ore_size * sqrt(2)

            inner_ore_radius = gen_circle_rad(diagonal=inner_ore_diagonal)
            second_ore_center, first_crossing = get_ore_center(first_ore_center, inner_ore_radius * 2)
            third_ore_center = get_ore_center(first_crossing, int(inner_ore_radius * 2))[0]
            fourth_ore_center = get_ore_center(first_crossing, int(inner_ore_radius * 2))[0]
            while dist(fourth_ore_center, third_ore_center) <= int(inner_ore_radius * 2):
                fourth_ore_center = get_ore_center(first_crossing, int(inner_ore_radius * 2))[0]

            ores_centers = [first_ore_center, second_ore_center, third_ore_center, fourth_ore_center]
            print(ores_centers)
            return ores_centers

        outer_ore_size = self.ore_size

        def gen_ore_centers():
            inner_ores_centers = gen_inner_ores_centers()

            outer_ore_diagonal = outer_ore_size * sqrt(2)

            blocked_square = (
                [basic_square_mtx_bounds[0][0] - outer_ore_size, basic_square_mtx_bounds[0][1] - outer_ore_size],
                [basic_square_mtx_bounds[1][0] + outer_ore_size, basic_square_mtx_bounds[1][1] + outer_ore_size])
            outer_ores_centers = []
            for ore in range(self.num_ores - 4):
                x, y = random_point_with_blocked_square(outer_ore_size, outer_ore_size, MAP_W - outer_ore_size,
                                                        MAP_H - outer_ore_size, blocked_square)
                for gen_ore_center in outer_ores_centers:
                    while dist((x, y), gen_ore_center) <= int(outer_ore_diagonal * 4):
                        x, y = random_point_with_blocked_square(outer_ore_size, outer_ore_size, MAP_W - outer_ore_size,
                                                                MAP_H - outer_ore_size, blocked_square)
                outer_ores_centers.append((x, y))

            inner_ores_bounds = []
            for ore_center in inner_ores_centers:
                inner_ores_bounds.append([[ore_center[0] - inner_ore_size_half, ore_center[1] - inner_ore_size_half],
                                          [ore_center[0] + inner_ore_size_half,
                                           ore_center[1] + inner_ore_size_half]])  # print(pic_mtx)

            outer_ore_size_half = outer_ore_size // 2
            outer_ores_bounds = []
            for ore_center in outer_ores_centers:
                outer_ores_bounds.append([[ore_center[0] - outer_ore_size_half, ore_center[1] - outer_ore_size_half],
                                          [ore_center[0] + outer_ore_size_half,
                                           ore_center[1] + outer_ore_size_half]])  # print(pic_mtx)
            return inner_ores_bounds, outer_ores_bounds

        inner_ores_bounds, outer_ores_bounds = gen_ore_centers()

        matrix = np.array([[0] * MAP_W] * MAP_H)
        print(outer_ores_bounds)

        batch_types = [IronBatch, CoalBatch, CopperBatch, StoneBatch]
        shuffle(batch_types)

        ores_with_types = []
        for idx, ore_bounds in enumerate(inner_ores_bounds):
            ores_with_types.append([ore_bounds, batch_types[idx]])

        for ore_bounds in outer_ores_bounds:
            ores_with_types.append([ore_bounds, choice(batch_types)])

        # TODO:
        """
        * gen_ore_matrix() - implement algo
        * generate surface_noise
        * interpret_surface_noise()
        """

        def interpret_surface_noise():
            pass

        def surface_noise():
            pass

        trees_matrix = gen_trees_map(self.height, self.width)

        for i in range(len(ores_with_types)):
            ores_with_types[i].append(gen_ore_matrix(self.ore_size))

        def create_batch_for_cell(x, y):
            for bounds, batch_type, ore_matrix in ores_with_types:
                if point_on_ore(x, y, bounds):
                    return batch_type(ore_matrix[x][y])

        for y in range(len(MAP_H)):
            for x in range(MAP_W):
                cell = MapCell(interpret_surface_noise(surface_noise[y][x]))
                # фабричны метод (зачем....)
                # raw_material_gen, amount = get_ore_of_cell(x, y)
                # if raw_material_gen:
                #     cell.raw_material_batch = raw_material_gen.generate_raw_material(amount)
                if trees_matrix[y][x]:
                    cell.raw_material_batch = TreeBatch(randint(10, 20))  # CONST
                else:
                    cell.raw_material_batch = create_batch_for_cell(x, y)
                self.map_matrix[y][x] = cell


class EasyMap(Map):
    def __init__(self):
        self.ore_size = 32
        self.inner_square_parts = [(10, 1, (800, 1000)),
                                   (16, 1, (600, 800)),
                                   (28, 0.6, (200, 600)),
                                   (32, 0.3, (0, 200)),
                                   ]
        self.radius_coef = (8, 10)
        self.num_ores = 10


class HardMap(Map):
    def __init__(self):
        self.ore_size = 28
        self.inner_square_parts = [(6, 1, (700, 900)),
                                   (12, 1, (500, 700)),
                                   (24, 0.6, (300, 500)),
                                   (28, 0.3, (0, 300)),
                                   ]


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


if __name__ == '__main__':
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
# for y in range(len(MAP_H)):
#     for x in range(MAP_W):
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
