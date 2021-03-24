from abc import ABC, abstractmethod
from constants import *
import numpy as np  # заблокируй себе import воздуха
from PIL import Image
from math import sin, cos, sqrt
from random import randint
from random_generator import random_point_with_blocked_square
from matplotlib import pyplot as plt

def abs_coordinates(x, y):
    return x + MAP_W // 2, y + MAP_H // 2


def dist(point1: tuple, point2: tuple) -> float:
    return sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def point_on_ore(x, y, ore):
    return ore[0][0] < x < ore[1][0] and ore[0][1] < y < ore[1][1]


class Map(ABC):
    height = MAP_H
    width = MAP_W
    map_matrix = [[0] * MAP_W] * MAP_H
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
        inner_square_mtx_bounds = (abs_coordinates(*inner_square_bounds[0]), abs_coordinates(*inner_square_bounds[1]))

        basic_square_size_half = 128  # CONST
        basic_square_bounds = (
            (-basic_square_size_half, -basic_square_size_half), (basic_square_size_half, basic_square_size_half))
        basic_square_mtx_bounds = (abs_coordinates(*basic_square_bounds[0]), abs_coordinates(*basic_square_bounds[1]))

        def gen_circle_rad(diagonal) -> int:
            return int((randint(*self.radius_coef) / 10) * diagonal)

        def dist(point1: tuple, point2: tuple) -> float:
            return sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

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
                    while dist((x, y), gen_ore_center) <= int(outer_ore_diagonal * 2):
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

        matix = np.array([[0] * MAP_W] * MAP_H)
        for ore in inner_ores_bounds:
            ore_matrix = np.array([[0] * self.ore_size] * self.ore_size)
            ore_matrix = np.random.rand(32, 32)
            ore_matrix = np.where(ore_matrix < 0.333, 0, np.random.rand(32, 32) * 300)
            # ore
            mt10 = (np.random.rand(10, 10) / 5 + 0.5) * 1000
            mt16 = np.zeros((16, 16))
            mt16[3:13, 3:13] = mt10
            mt16 = np.where(mt16 == 0, (np.random.rand(16, 16) / 5 + 0.3) * 1000, mt16)
            mt28 = np.zeros((28, 28))
            mt28[6:22, 6:22] = mt16
            # possib28 = np.random.rand(28, 28) * 0.6
            mt28 = np.where((mt28 == 0), ((np.random.rand(28, 28) / 2.5 + 0.2) - 0.4) * 1000, mt28)
            mt28 = np.where((mt28 < 0),0, mt28)

            mt32 = -np.ones((32, 32))
            mt32[2:30, 2:30] = mt28
            # possib32 = np.random.rand(32, 32) * 0.3
            mt32 = np.where((mt32 == -1), (np.random.rand(32, 32) / 5) * 1000, mt32)
            plt.imshow(mt32)
            plt.show()
        # ores_bounds = inner_ores_bounds + outer_ores_bounds
        # pic_mtx = np.array([[0] * MAP_W] * MAP_H)
        # for y in range(len(mt16)):
        #     for x in range(len(mt16[y])):
        # #         for i in range(len(ores_bounds)):
        # #             if point_on_ore(x, y, ores_bounds[i]):
        # #                 pic_mtx[y][x] = 50 if i < 4 else 70
        # # if point_on_ore(x, y, basic_square_mtx_bounds):
        # #     pic_mtx[y][x] += 10
        #
        # Image.fromarray(pic_mtx).show()


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


creator = EasyMapCreator()
creator.gen_map()
