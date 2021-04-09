from abc import ABC, abstractmethod
import random
from core.generators.trees_generator import gen_trees_map
from core.generators.surface_generator import gen_surface_map
from core.generators.ores_generator import OresGenerator
from core.virtual_objects.raw_materials.raw_materials import TreeBatch, WaterBatch
import constants as const


class MapCell:
    __slots__ = {"category", "usable_object", "raw_material_batch"}

    def __init__(self, category: str):
        self.category: str = category
        self.usable_object = None
        self.raw_material_batch = None

    def __str__(self):
        return f"{self.category}, {type(self.raw_material_batch)}"


class Map(ABC):
    height = const.MAP_H
    width = const.MAP_W
    ore_size: int
    num_ores: int
    radius_coefficient_bounds: tuple
    map_objects: dict

    def __init__(self):
        self.map_objects = {}
        self.map_matrix = [
            [None for __ in range(self.width)] for _ in range(self.height)
        ]

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
                if generated_batch:
                    if isinstance(generated_batch, WaterBatch):
                        cell.raw_material_batch = WaterBatch()
                    else:
                        cell.raw_material_batch = generated_batch
                if trees_matrix[y][x] and not cell.raw_material_batch:
                    cell.raw_material_batch = TreeBatch(random.randint(10, 20))  # CONST
                cell_id = id(cell)
                self.map_matrix[y][x] = cell_id
                self.map_objects[cell_id] = cell


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
