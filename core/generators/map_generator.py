import numpy as np
from random import randint
from math import sin, cos, sqrt
from constants import *
from copy import deepcopy
from random_generator import random_point_with_blocked_square
from PIL import Image
from random import shuffle

import time

cell_len = 1  # CONST
NUM_ORES = 14  # CONST


# MAP_H = 40 * cell_len
# MAP_W = 70 * cell_len
def timeit(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        func_return_val = func(*args, **kwargs)
        end = time.perf_counter()
        name = func.__name__.upper()
        print(f'{name} TIME: {end - start}')
        return func_return_val

    return wrapper


def abs_coordinates(x, y):
    return x + MAP_W // 2, y + MAP_H // 2


# inner_square_bounds = np.array([[-128, -128], [128, 128]])
inner_ore_size = 32  # CONST
inner_ore_size_half = inner_ore_size // 2

outer_ore_size = 20  # CONST

inner_square_size = inner_ore_size * 2  # changed
inner_square_size_half = inner_square_size // 2
inner_square_bounds = (
    (-inner_square_size_half, -inner_square_size_half), (inner_square_size_half, inner_square_size_half))
inner_square_mtx_bounds = (abs_coordinates(*inner_square_bounds[0]), abs_coordinates(*inner_square_bounds[1]))

basic_square_size_half = 128  # CONST
basic_square_bounds = (
    (-basic_square_size_half, -basic_square_size_half), (basic_square_size_half, basic_square_size_half))
basic_square_mtx_bounds = (abs_coordinates(*basic_square_bounds[0]), abs_coordinates(*basic_square_bounds[1]))

radius_coef = (8, 10)  # CONST


def gen_circle_rad(diagonal) -> int:
    return int((randint(*radius_coef) / 10) * diagonal)


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

    inner_ore_diagonal = inner_ore_size * sqrt(2)

    inner_ore_radius = gen_circle_rad(diagonal=inner_ore_diagonal)
    second_ore_center, first_crossing = get_ore_center(first_ore_center, inner_ore_radius * 2)
    third_ore_center = get_ore_center(first_crossing, int(inner_ore_radius * 2))[0]
    fourth_ore_center = get_ore_center(first_crossing, int(inner_ore_radius * 2))[0]
    while dist(fourth_ore_center, third_ore_center) <= int(inner_ore_radius * 2):
        fourth_ore_center = get_ore_center(first_crossing, int(inner_ore_radius * 2))[0]

    ores_centers = [first_ore_center, second_ore_center, third_ore_center, fourth_ore_center]
    print(ores_centers)
    return ores_centers


@timeit
def gen_ore_centers():
    inner_ores_centers = gen_inner_ores_centers()

    outer_ore_diagonal = outer_ore_size * sqrt(2)

    blocked_square = ([basic_square_mtx_bounds[0][0] - outer_ore_size, basic_square_mtx_bounds[0][1] - outer_ore_size],
                      [basic_square_mtx_bounds[1][0] + outer_ore_size, basic_square_mtx_bounds[1][1] + outer_ore_size])
    outer_ores_centers = []
    for ore in range(NUM_ORES - 4):
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

    outer_ores_bounds = []
    for ore_center in outer_ores_centers:
        outer_ores_bounds.append([[ore_center[0] - outer_ore_size, ore_center[1] - outer_ore_size],
                                  [ore_center[0] + outer_ore_size, ore_center[1] + outer_ore_size]])  # print(pic_mtx)
    return inner_ores_bounds, outer_ores_bounds

    #  VIS


inner_ores_bounds, outer_ores_bounds = gen_ore_centers()
ores_bounds = inner_ores_bounds + outer_ores_bounds
pic_mtx = np.array([[0] * MAP_W] * MAP_H)
for y in range(len(pic_mtx)):
    for x in range(len(pic_mtx[y])):
        for i in range(len(ores_bounds)):
            if point_on_ore(x, y, ores_bounds[i]):
                pic_mtx[y][x] = 50 if i < 4 else 70
if point_on_ore(x, y, basic_square_mtx_bounds):
    pic_mtx[y][x] += 10

Image.fromarray(pic_mtx).show()
# inner_ores_bounds, outer_ores_bounds = gen_ore_centers()
#
# map_matrix = np.zeros((MAP_H, MAP_W))
#
# ores_types = ['iron', 'copper', 'stone', 'coal']
# shuffle(ores_types)
# ores_matrices = {}
#
#
# def gen_inner_ore_matrix():
#
#
# def gen_outer_ore_matrix():
#     pass
#
#
# for idx, inner_ore in enumerate(inner_ores_bounds):
#     ores_matrices[ores_types[idx]] = gen_inner_ore_matrix(inner_ore)
#
# for idx, outer_ore in enumerate(outer_ores_bounds):
#     ores_matrices[ores_types[randint(0, 3)]] = gen_outer_ore_matrix(outer_ore)
