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
    def __init__(self, object_type, amount):
        super().__init__(amount)
        self.object_type = object_type

    def put_map_object(self, x, y, created_object, real_map: Map):
        cell = real_map.get_cell(x, y)
        cell.usable_object = created_object
        # real_map.set_cell(x, y, cell)
        self.amount -= 1

    @abstractmethod
    def create_object(self, x, y, real_map: Map):
        pass


class MachineCreator(MapObjectCreator):
    def create_object(self, x, y, real_map: Map):
        self.put_map_object(x, y, self.object_type(x, y), real_map)


class DrillCreator(MapObjectCreator):
    def create_object(self, x, y, real_map: Map):
        self.put_map_object(
            x, y, self.object_type(x, y, real_map.get_cell(x, y)), real_map
        )


class ElectricPoleCreator(MapObjectCreator):
    def create_object(self, x, y, map_obj: Map):
        created_pole: ElectricPole = self.object_type(x, y)
        self.put_map_object(x, y, created_pole, map_obj)


class GeneratorCreator(MapObjectCreator):
    def create_object(self, x, y, map_obj: Map):
        created_generator = self.object_type(x, y)
        self.put_map_object(x, y, created_generator, map_obj)
