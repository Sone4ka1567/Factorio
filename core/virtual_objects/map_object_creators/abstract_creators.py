from math import sqrt
from abc import ABC, abstractmethod

from maps import Map
from base_classes import VirtualObject
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

        nearest_pole = find_nearest(
            x, y, self.object_type.wire_len, map_obj, ElectricPole
        )
        if nearest_pole:
            created_pole.connect_to_network(nearest_pole.network)
        else:
            nearest_generator = find_nearest(
                x, y, self.object_type.wire_len, map_obj, BurnerElectricGenerator
            )
            if nearest_generator:
                created_pole.connect_to_network(nearest_generator.network)
            else:
                el_net = ElectricNetwork(map_obj)
                map_obj.add_network(el_net)
                created_pole.connect_to_network(el_net)

        for dx in range(-created_pole.coverage_rad, created_pole.coverage_rad):
            for dy in range(-created_pole.coverage_rad, created_pole.coverage_rad):
                if dx == 0 and dy == 0:
                    continue
                obj = map_obj.get_cell(x + dx, y + dy).usable_object
                if (
                        isinstance(obj, Machine)
                        and isinstance(obj.energy_source, ElectricPowerSource)
                        and obj.energy_source.power is None
                ):
                    obj.energy_source.put_energy(created_pole.network.power)

        self.put_map_object(x, y, created_pole, map_obj)


class GeneratorCreator(MapObjectCreator):
    def create_object(self, x, y, map_obj: Map):
        created_generator = self.object_type(x, y)

        nearest_pole = find_nearest(
            x,
            y,
            self.object_type.wire_len,
            map_obj,
            ElectricPole,
        )
        if nearest_pole:
            created_generator.connect_to_network(nearest_pole.network)
        else:
            el_net = ElectricNetwork(map_obj)
            created_generator.connect_to_network(el_net)
            map_obj.add_network(el_net)

        self.put_map_object(x, y, created_generator, map_obj)
