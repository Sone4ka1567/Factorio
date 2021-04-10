from base_classes import VirtualObject
from abc import abstractmethod
from core.virtual_objects.container import Container


class MaterialBatch(VirtualObject):
    def __init__(self, amount):
        self.amount = amount

    def __copy__(self):
        return MaterialBatch(self.amount)

    @abstractmethod
    def count_requirements(self, container: Container):
        pass

    def __str__(self):
        return f'{self.__class__.__name__}: {self.amount}'
