from abc import abstractmethod, ABC

from core.map_objects.abstracts import UsableObjectProxy
from core.map_objects.abstracts import UsableObject
from core.container import Container

from core.virtual_objects.materials.raw_and_basics import *
from core.virtual_objects.materials.intermediates import *


class EnergySource(ABC):
    @abstractmethod
    def check_energy(self):
        pass

    @abstractmethod
    def subtract_energy(self):
        pass


class BurnerEnergySource(EnergySource):
    def __init__(self):
        self.fuel = Container(1)
        self.fuel.put(Coal(10))

    def check_energy(self):
        return not self.fuel.is_empty()

    def subtract_energy(self):
        self.fuel.remove(self.fuel[0].get_n(1))


class Machine(ABC):
    input_slots_num: int
    producing_bar = 0
    energy_source: EnergySource
    valid_input: list

    def __init__(self):
        self.input = Container(self.input_slots_num)
        self.output = Container(1)

    def put_input(self, batch):
        if type(batch) in self.valid_input:
            return self.input.put(batch)
        return False

    def remove_input(self, batch):
        self.input.remove(batch)

    def remove_output(self, batch):
        self.output.remove(batch)

    @abstractmethod
    def process(self):
        pass


# todo: класть топливо

class Furnace(Machine, ABC):
    input_slots_num = 1

    def __init__(self):
        super().__init__()
        self.producing_bar = 0
        self.target_type = None

    def process(self):
        if not self.energy_source.check_energy():
            return
        if self.producing_bar == 0:
            if self.input.is_empty():
                return
            input_batch = self.input[0]
            self.target_type = input_batch.associated_basic
            self.input.remove(input_batch.get_n(1))
            self.producing_bar += 1
        else:
            self.energy_source.subtract_energy()
            if self.producing_bar == self.target_type.ticks_to_produce:
                self.output.put(self.target_type(1))
                self.producing_bar = 0
            else:
                self.producing_bar += 1
        print(f'prog: {self.producing_bar}, input: {self.input}, output: {self.output}')


class BurnerFurnace(Furnace):
    valid_input = [Coal, Iron]

    def __init__(self):
        super().__init__()
        self.energy_source = BurnerEnergySource()
