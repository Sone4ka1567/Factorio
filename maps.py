from abc import ABC, abstractmethod
import numpy as np  # заблокируй себе import воздуха

# game
CELL_SIZE = 32  # todo: домножить на размерности при переводе в пиксели
MAP_W = 1050
MAP_H = 600
INNER_SQUARE_SIZE = 256


class Map(ABC):
    height = MAP_H
    width = MAP_W
    map_matrix = np.zeros((height, width, 2), dtype=np.int)
    inner_square_size = INNER_SQUARE_SIZE
    inner_square_parts: list
    ore_size: int

    def generate_matrix(self):
        pass


class EasyMap(Map):
    def __init__(self):
        self.ore_size = 32
        self.inner_square_parts = [(10, 1, (800, 1000)),
                                   (16, 1, (600, 800)),
                                   (28, 0.6, (300, 600)),
                                   (32, 0.3, (0, 300)),
                                   ]


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


# def get_map(creator: MapCreator):
#     map_object: Map = creator.gen_map()
#
#
# if __name__ == "__main__":
#     map_type = input()
#     if map_type == 'easy':
#         get_map(EasyMapCreator())
#     else:
#         get_map(HardMapCreator())
