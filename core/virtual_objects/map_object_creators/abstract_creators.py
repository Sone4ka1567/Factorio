from math import sqrt
from abc import ABC, abstractmethod

from maps import Map
from virtual_object import VirtualObject
from core.map_objects.production.electricity import (
    ElectricPole,
    ElectricNetwork,
    BurnerElectricGenerator,
)
from core.map_objects.production.production import Machine
from core.map_objects.production.power_source import ElectricPowerSource
from core.virtual_objects.materials.intermediates import Intermediate
import core.virtual_objects.materials.intermediates as inter
import core.virtual_objects.materials.raw_and_basics as rnb


def create_virtual_object(object_type, n):
    return object_type(n)


class MapObjectCreator(Intermediate):
    def __init__(self, object_type, amount, map_obj: Map):
        super().__init__(amount)
        self.object_type = object_type
        self.map_obj = map_obj

    def _put_map_object(self, x, y, created_object, real_map: Map):
        cell = real_map.get_cell(x, y)
        cell.usable_object = created_object
        # real_map.set_cell(x, y, cell)
        self.amount -= 1

    def create_object(self, x, y):
        self._put_map_object(x, y, self.object_type(x, y), self.map_obj)
