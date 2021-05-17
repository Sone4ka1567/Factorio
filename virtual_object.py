from abc import ABC


class VirtualObject(ABC):
    def __init__(self, amount):
        self.amount = amount

    def get_displayable_name(self):
        return self.__class__.__name__
