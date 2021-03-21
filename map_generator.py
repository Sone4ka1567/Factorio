import numpy as np
from random import randint
from math import sin, cos, sqrt
from copy import deepcopy
from random_generator import random_from_done_intervals
from PIL import Image

cell_len = 1

map_h = 600 * cell_len
map_w = 1050 * cell_len
# map_h = 40 * cell_len
# map_w = 70 * cell_len

raw_materials = {'iron': 1, 'copper': 2, 'coal': 3, 'stone': 4}


def abs_coordinates(x, y):
    return x + map_w // 2, y + map_h // 2


# inner_square_bounds = np.array([[-128, -128], [128, 128]])

inner_ore_size = 32
inner_ore_size_half = inner_ore_size // 2

inner_square_size = inner_ore_size * 2  # changed
inner_square_size_half = inner_square_size // 2
inner_square_bounds = (
    (-inner_square_size_half, -inner_square_size_half), (inner_square_size_half, inner_square_size_half))
inner_square_mtx_bounds = (abs_coordinates(*inner_square_bounds[0]), abs_coordinates(*inner_square_bounds[1]))

basic_square_size_half = 128
basic_square_bounds = (
    (-basic_square_size_half, -basic_square_size_half), (basic_square_size_half, basic_square_size_half))
basic_square_mtx_bounds = (abs_coordinates(*basic_square_bounds[0]), abs_coordinates(*basic_square_bounds[1]))


def my_print(mtx):
    for y_line in mtx:
        for x in y_line:
            print(x, end=' ')
        print()


from time import time

for _ in range(10):
    t = time()
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


    def gen_circle_rad():
        return int((randint(8, 10) / 10) * inner_ore_diagonal)


    def dist(point1: tuple, point2: tuple):
        return sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


    r = gen_circle_rad()
    second_ore_center, first_crossing = get_ore_center(first_ore_center, r * 2)
    third_ore_center = get_ore_center(first_crossing, int(r * 2))[0]
    fourth_ore_center = get_ore_center(first_crossing, int(r * 2))[0]
    while dist(fourth_ore_center, third_ore_center) <= int(r * 2):
        fourth_ore_center = get_ore_center(first_crossing, int(r * 2))[0]

    ores_centers = [first_ore_center, second_ore_center, third_ore_center, fourth_ore_center]
    print(ores_centers)
    ores_bounds = []
    for ore_center in ores_centers:
        ores_bounds.append([[ore_center[0] - inner_ore_size_half, ore_center[1] - inner_ore_size_half],
                            [ore_center[0] + inner_ore_size_half, ore_center[1] + inner_ore_size_half]])

    pic_mtx = np.zeros((map_h, map_w))


    def point_on_ore(x, y, ore):
        return ore[0][0] < x < ore[1][0] and ore[0][1] < y < ore[1][1]


    # for y in range(len(pic_mtx)):
    #     for x in range(len(pic_mtx[y])):
    #         for i in range(len(ores_bounds)):
    #             if point_on_ore(x, y, ores_bounds[i]):
    #                 pic_mtx[y][x] = (i + 1) * 30
    #             if point_on_ore(x, y, basic_square_mtx_bounds):
    #                 pic_mtx[y][x] += 20
    print(time() - t)
    # Image.fromarray(pic_mtx).show()
    # Image.fromarray(pic_mtx // 3).save('test/' + str(_) + '.png', format='png')
exit()
# print(pic_mtx)
# Image.fromarray(pic_mtx).show()
# big_square_left = first_ore_center[0] - 3 * inner_ore_size
# big_square_right = first_ore_center[0] + 3 * inner_ore_size
# big_square_top = first_ore_center[1] + 3 * inner_ore_size
# big_square_bottom = first_ore_center[1] - 3 * inner_ore_size
#
# next_centers = []
# if big_square_left > inner_square_mtx_bounds[0][0]:
#     if big_square_top < inner_square_mtx_bounds[1][1]:
#         if big_square_bottom > inner_square_mtx_bounds[0][1]:
#             next_centers.append(())

# class MapGenerator:
#     def __init__(self):
#         self.map_matrix = np.zeros((map_h, map_w, 2), dtype=np.int)  # [[[300, 1], [200, 1], [100, 1], [0, 0]]]
#         self.done_x_intervals = []
#         self.done_y_intervals = []
#
#     def gen_inner_ore_bounds(self):
#         center_x = random_from_done_intervals(
#             inner_square_abs_bounds[0][0], inner_square_abs_bounds[1][0],
#             self.done_x_intervals,
#             inner_ore_size)
#         center_y = random_from_done_intervals(
#             inner_square_abs_bounds[0][1], inner_square_abs_bounds[1][1],
#             self.done_y_intervals,
#             inner_ore_size)
#         center = (center_x, center_y)
#         bounds = np.array([[center[0] - inner_ore_size_half, center[1] - inner_ore_size_half],
#                            [center[0] + inner_ore_size_half, center[1] + inner_ore_size_half]])
#         self.done_x_intervals.append((bounds[0][0], bounds[1][0]))
#         self.done_y_intervals.append((bounds[0][1], bounds[1][1]))
#         return bounds
#
#     def generate_matrix(self):
#         # for ore_type in raw_materials.keys():
#         ore_bounds = self.gen_inner_ore_bounds()
#         self.map_matrix[ore_bounds[0][1]: ore_bounds[1][1], ore_bounds[0][0]: ore_bounds[1][0]] = \
#             np.ones((inner_ore_size, inner_ore_size, 2), dtype=np.int)
#         # my_print(self.map_matrix)
#         pic_mtx = np.zeros((map_h, map_w))
#         x_left, y_left = (inner_square_abs_bounds[0][0], inner_square_abs_bounds[0][1])
#         x_right, y_right = (inner_square_abs_bounds[1][0], inner_square_abs_bounds[1][1])
#         print(x_left, y_left)
#         print(x_right, y_right)
#         for i in range(len(pic_mtx)):
#             for j in range(len(pic_mtx[i])):
#
#                 # print(x_left, y_left)
#                 # print(x_right, y_right)
#                 if np.array(self.map_matrix[i][j][1]):
#                     pic_mtx[i][j] = 55
#                 elif i > y_left and j > x_left and i < y_right and j < x_right:
#                     pic_mtx[i][j] = 99
#
#         # print(pic_mtx)
#         Image.fromarray(pic_mtx).show()


# map_gen = MapGenerator()
# map_gen.generate_matrix()
