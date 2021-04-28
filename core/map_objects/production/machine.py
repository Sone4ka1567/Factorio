from abc import abstractmethod, ABC

from core.container import Container

from core.map_objects.production.power_source import PowerSource


class Machine(ABC):
    input_slots_num: int
    progress = 0
    energy_source: PowerSource
    valid_input: tuple
    energy_consumption: int
    speed: int
    ticks_per_batch = 10

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

    def put_energy(self, *args):
        return self.energy_source.put_energy(*args)

    @abstractmethod
    def process(self):
        pass

    def disable(self):
        self.energy_source.finish_using()

    def __str__(self):
        return f"input: {self.input}, output: {self.output}, power: {self.energy_source.amount()}"
