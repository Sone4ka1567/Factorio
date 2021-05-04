from abc import ABC, abstractmethod


class MapObject(ABC):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def replace(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def to_json(self):
        return {"type": self.__class__.__name__, "x": self.x, "y": self.y}

    @abstractmethod
    def process(self):
        pass


class VirtualObject(ABC):
    def __init__(self, amount):
        self.amount = amount
