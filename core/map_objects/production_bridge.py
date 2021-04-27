from core.map_objects.abstracts import UsableObjectProxy
from core.map_objects.abstracts import UsableObject
from core.container import Container
#
# from core.virtual_objects.materials.raw_and_basics import *
#
# from abc import abstractmethod
# from core.virtual_objects.materials.intermediates import *
from abc import abstractmethod

from typing import Tuple


class PowerSource:
    @abstractmethod
    def has_power(self):
        pass


class ElectricPowerSource(PowerSource):
    def has_power(self):
        return False


class BurnerPowerSource(PowerSource):
    def has_power(self):
        return True


class Machine(UsableObject):
    input_slots: int
    possible_input: list
    power_source: PowerSource

    def __init__(self, x, y):
        super().__init__(x, y)
        self.input = Container(self.input_slots)
        self.output = Container(1)

    def put_input(self, batch):
        res = self.input.put(batch)
        return res

    def remove_input(self, batch):
        self.input.remove(batch)

    @abstractmethod
    def process(self):
        pass


class Furnace(Machine):
    crafting_speed: int

    def process(self):
        print(self.power_source.has_power())
        print('processing')


class BurnerFurnace(Furnace):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.power_source = BurnerPowerSource()
        self.speed = 0.5
        self.area = (1, 1)


class ElectricFurnace(Furnace):
    def __init__(self):
        self.power_source = ElectricPowerSource()
        self.speed = 0.8
        self.area = (2, 2)


class AssemblingMachine:
    crafting_speed: int

    def process(self):
        print('suka')


class BurnerAssemblingMachine:
    def __init__(self, x, y):
        super().__init__(x, y)
        self.power_source = BurnerPowerSource()
        self.speed = 0.5
        self.area = (1, 1)
