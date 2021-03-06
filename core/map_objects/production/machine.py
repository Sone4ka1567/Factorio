from abc import abstractmethod, ABC

from core.container import Container

from core.map_objects.production.power_source import PowerSource, ElectricPowerSource
from map_object import MapObject


class Machine(MapObject, ABC):
    input_slots_num: int = 1
    progress: int = 0
    energy_source: PowerSource = None
    valid_input: tuple = tuple()
    energy_consumption: int = 1
    speed: int = 1
    ticks_per_batch: int = 10

    def __init__(self, x, y, map_obj):
        super().__init__(x, y, map_obj)
        self.input = Container(self.input_slots_num)
        self.output = Container(1)

    def put_input(self, batch):
        if type(batch) in self.valid_input:
            return self.input.put(batch)
        return False

    def get_output(self):
        return self.output

    def remove_input(self, batch):
        self.input.remove(batch)

    def remove_output(self, batch):
        self.output.remove(batch)

    def clear_output(self):
        self.output = Container(1)

    def put_energy(self, *args):
        return self.energy_source.put_energy(*args)

    def remove_energy(self):
        self.energy_source.remove_energy()

    def disable(self):
        self.energy_source.finish_using()

    def has_energy(self):
        return self.energy_source.has_energy()

    def __str__(self):
        return f"type: {self.__class__.__name__}, input: {self.input}, output: {self.output}, power: {self.energy_source.amount()}"

    @staticmethod
    def needs_energy():
        return True

    def needs_electric_energy(self):
        return isinstance(self.energy_source, ElectricPowerSource)
