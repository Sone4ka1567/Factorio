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
from core.generators.ore_generator import OresGenerator
from core.virtual_objects.raw_materials.raw_materials import (
    TreeBatch,
    WaterBatch
)


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
    radius_coefficient_bounds: tuple

    def __init__(self):
        self.map_matrix = [[None for __ in range(self.width)] for _ in range(self.height)]

    def generate_matrix(self):

        # TODO:
        """
        * gen_ore_matrix() - implement algo
        * test all
        """

        trees_matrix = gen_trees_map(self.height, self.width)
        surface_noise = gen_surface_noise(self.height, self.width)
        plt.imshow(surface_noise)
        plt.show()

        def interpret_surface_noise(el):
            return "dark" if el == 1 else 'light'

        ores_gen = OresGenerator(radius_coefficient_bounds=self.radius_coefficient_bounds,
                                 ore_size=self.ore_size,
                                 num_ores=self.num_ores,
                                 map_width=self.width,
                                 map_height=self.height)
        for y in range(self.height):
            for x in range(self.width):
                cell = MapCell(interpret_surface_noise(surface_noise[y][x]))
                generated = ores_gen.create_batch_for_cell(x, y)
                if generated and isinstance(generated, WaterBatch):
                    cell.raw_material_batch = WaterBatch()
                elif trees_matrix[y][x]:
                    cell.raw_material_batch = TreeBatch(random.randint(10, 20))  # CONST
                else:
                    cell.raw_material_batch = generated
                self.map_matrix[y][x] = cell
        # print(self.map_matrix[10:][10:])

    def plot(self):
        categories = {'dark': 13, 'light': 15}
        map_objects = {'IronBatch': 1, 'CopperBatch': 3, 'CoalBatch': 5, 'StoneBatch': 7, 'TreeBatch': 9,
                       'WaterBatch': 11}
        res = np.zeros((self.height, self.width))
        for y in range(self.height):
            for x in range(self.width):
                cell: MapCell = self.map_matrix[y][x]
                # print(cell)
                res[y][x] = categories[cell.category]
                if cell and cell.raw_material_batch:
                    # res[y][x] = map_objects[cell.raw_material_batch.__class__.__name__]
                    if cell.raw_material_batch.__class__.__name__ in ['IronBatch','CopperBatch', 'CoalBatch', 'StoneBatch']:
                        res[y][x] = cell.raw_material_batch.amount / 100
                    else:
                        res[y][x] = map_objects[cell.raw_material_batch.__class__.__name__]


            #     print(b.category, end=' ')
            # print()
        plt.imshow(res)
        plt.show()


class EasyMap(Map):
    def __init__(self):
        super().__init__()
        self.ore_size = 32
        self.radius_coefficient_bounds = (0.8, 1)
        self.num_ores = 12


class HardMap(Map):
    def __init__(self):
        super().__init__()
        self.ore_size = 28
        self.radius_coefficient_bounds = (1, 1.2)
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
    for i in range(1):
        creator = EasyMapCreator()
        map = creator.gen_map()
        map.plot()
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
