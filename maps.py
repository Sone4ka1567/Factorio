from abc import ABC, abstractmethod
import random
import numpy as np
from core.generators.trees_generator import gen_trees_map
from core.generators.surface_generator import gen_surface_map
from core.generators.ores_generator import OresGenerator
from core.virtual_objects.materials.raw_and_basics import Wood
import constants as const
import json as json_lib
from core.virtual_objects.materials import raw_and_basics


class MapCell:
    __slots__ = {"category", "usable_object", "raw_material_batch"}

    def __init__(self, category="light", json=None):
        if json:
            self.category = json["category"]
            self.raw_material_batch = (
                None
                if not json["batch"]
                else getattr(raw_and_basics, json["batch"]["type"])(
                    json["batch"]["amount"]
                )
            )
            self.usable_object = None
        else:
            self.category: str = category
            self.usable_object = None
            self.raw_material_batch = None

    def __str__(self):
        return f"{self.category}, {self.raw_material_batch}, {self.usable_object.__class__.__name__}"

    def to_json(self):
        return {
            "category": self.category,
            "batch": self.raw_material_batch.to_json()
            if self.raw_material_batch
            else None,
            "usable_object": self.usable_object.to_json()
            if self.usable_object
            else None,
        }


class Map(ABC):
    height = const.MAP_H
    width = const.MAP_W
    ore_size: int
    num_ores: int
    radius_coefficient_bounds: tuple
    map_objects: dict
    map_matrix: np.ndarray

    def __init__(self):
        self.map_objects = {}
        self.map_matrix = np.zeros((self.height, self.width), dtype=np.int64)

    def get_map_objects(self):
        return self.map_objects

    def get_map_matrix(self):
        return self.map_matrix

    def get_cell(self, x, y):
        # x, y = self.get_mtx_coordinates(x, y)
        return self.map_objects[self.map_matrix[y][x]]

    # def set_cell(self, x, y, cell: MapCell):
    #     x, y = self.get_mtx_coordinates(x, y)
    #     cell_id = id(cell)
    #     self.map_matrix[y][x] = cell_id
    #     self.map_objects[cell_id] = cell

    @staticmethod
    def get_mtx_coordinates(x, y):
        return OresGenerator.mtx_coordinates(x, y)

    def generate_matrix(self):
        trees_matrix = gen_trees_map(self.height, self.width)
        surface_noise = gen_surface_map(self.height, self.width)

        ores_gen = OresGenerator(
            radius_coefficient_bounds=self.radius_coefficient_bounds,
            ore_size=self.ore_size,
            num_ores=self.num_ores,
            map_width=self.width,
            map_height=self.height,
        )

        for y in range(self.height):
            for x in range(self.width):
                surface_cat = "dark" if surface_noise[y][x] == 1 else "light"
                cell = MapCell(category=surface_cat)
                generated_batch = ores_gen.create_batch_for_cell(x, y)
                if generated_batch and generated_batch.amount != 0:
                    cell.raw_material_batch = generated_batch
                if trees_matrix[y][x] and not cell.raw_material_batch:
                    cell.raw_material_batch = Wood(random.randint(10, 20))  # CONST
                cell_id = id(cell)
                self.map_matrix[y][x] = cell_id
                self.map_objects[cell_id] = cell

    def serialize(self):
        res = [[None for _ in range(self.width)] for __ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                res[y][x] = self.map_objects[self.map_matrix[y][x]].to_json()
        with open("map.json", "w+") as f:
            json_lib.dump(res, f)

    def load(self, json):
        for y in range(self.height):
            for x in range(self.width):
                cell = MapCell(json=json[y][x])
                cell_id = id(cell)
                self.map_objects[cell_id] = cell
                self.map_matrix[y][x] = cell_id

    def get_usable_object(self, x, y):
        return self.map_objects[self.map_matrix[y][x]].usable_object

    def plot(self):
        import numpy as np
        import matplotlib.pyplot as plt
        categories = {'dark': 13, 'light': 15}
        map_objects = {'Iron': 1, 'Copper': 3, 'Coal': 5, 'Stone': 7, 'Wood': 9,
                       'Silicon': 11}
        res = np.zeros((self.height, self.width))
        for y in range(self.height):
            for x in range(self.width):
                cell: MapCell = self.map_objects[self.map_matrix[y][x]]
                # print(cell)
                res[y][x] = categories[cell.category]
                if cell and cell.raw_material_batch:
                    # res[y][x] = map_objects[cell.raw_material_batch.__class__.__name__]
                    if cell.raw_material_batch.__class__.__name__ in ['Iron', 'Copper', 'Coal',
                                                                      'Stone', 'Silicon']:
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
        map_obj = creator.gen_map()
        from pympler.asizeof import asizeof

        print(asizeof(map_obj))
