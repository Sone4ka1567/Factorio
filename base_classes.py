from abc import ABC


class MapObject(ABC):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def replace(self, new_x, new_y):
        self.x = new_x
        self.y = new_y


class VirtualObject(ABC):
    def __init__(self, amount):
        self.amount = amount
