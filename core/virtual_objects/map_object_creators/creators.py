from typing import List

from base_classes import VirtualObject
from abc import ABC, abstractmethod
from maps import Map
from core.map_objects.production.electricity import ElectricPole, ElectricNetwork
from core.map_objects.production.production import Machine
from core.map_objects.production.power_source import ElectricPowerSource
from math import sqrt


def create_virtual_object(object_type, n):
    return object_type(n)


class MapObjectCreator(VirtualObject, ABC):
    def put_map_object(self, x, y, created_object, real_map: Map):
        cell = real_map.get_cell(x, y)
        cell.usable_object = created_object
        real_map.set_cell(x, y, cell)
        self.amount -= 1

    @abstractmethod
    def create_object(self, *args):
        pass


class MachineCreator(MapObjectCreator):
    def create_object(self, x, y, machine_type, real_map: Map):
        self.put_map_object(x, y, machine_type(x, y), real_map)


class PoleCreator(MapObjectCreator):
    def create_object(
            self, x, y, pole_type, map_obj: Map, networks: List[ElectricNetwork]
    ):
        dist_coordinates = {}
        half_len = pole_type.wire_len // 2
        created_pole: ElectricPole = pole_type(x, y)

        for dx in range(-half_len, half_len):
            for dy in range(-half_len, half_len):
                if dx == 0 and dy == 0:
                    continue
                obj = map_obj.get_cell(x + dx, y + dy).usable_object
                if isinstance(obj, ElectricPole):
                    dist_coordinates = {sqrt(dx ** 2 + dy ** 2): obj}
        if not dist_coordinates:
            el_net = ElectricNetwork()
            networks.append(el_net)
            created_pole.connect_to_network(el_net)
        else:
            nearest_pole = dist_coordinates[min(dist_coordinates.keys())]
            nearest_pole.network.add_pole(created_pole)
            created_pole.connect_to_network(nearest_pole.network)

        half_coverage = pole_type.coverage // 2
        for dx in range(-half_coverage, half_coverage):
            for dy in range(-half_coverage, half_coverage):
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
