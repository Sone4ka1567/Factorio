from abc import ABC, abstractmethod
from maps import Map


class MapObject(ABC):
    def __init__(self, x, y, map_obj: Map):
        self.x = x
        self.y = y
        self.map_obj = map_obj

    def replace(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def to_json(self):
        return {"type": self.__class__.__name__, "x": self.x, "y": self.y}

    @abstractmethod
    def process(self):
        pass

    def _clear_cell(self):
        cell = self.map_obj.get_cell(self.x, self.y)
        cell.usable_object = None

    def remove(self):
        self._clear_cell()



class VirtualObject(ABC):
    def __init__(self, amount):
        self.amount = amount
