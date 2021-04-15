from core.map_objects.abstracts import UsableObjectProxy
from core.map_objects.abstracts import UsableObject
from core.container import Container

from core.virtual_objects.materials.raw_and_basics import *
from core.virtual_objects.materials.intermediates import *


class Machine(UsableObjectProxy):
    input_slots: int
    possible_targets: list
    target: type

    def __init__(self, real_object: UsableObject):
        super().__init__(real_object)
        self.input = Container(self.input_slots)
        self.output = Container(1)

    def put_input(self, batch):
        res = self.input.add(batch)
        return res

    def remove_input(self, batch):
        self.input.remove(batch)

    def remove_output(self, batch):
        self.output.remove(batch)

    def get_possible_targets(self):
        return self.possible_targets

    def set_target(self, batch_type):
        self.target = batch_type

    def process(self):
        pass


class BurnerMachine(Machine):
    def __init__(self, real_object: UsableObject):
        super().__init__(real_object)
        self.fuel = Container(1)

    def put_fuel(self, batch):
        if isinstance(batch, (Coal, Wood)):  # decorate?
            res = self.fuel.add(batch)
            return res
        return False

    def remove_fuel(self, batch):
        self.fuel.remove(batch)


class AssemblingMachine(BurnerMachine):
    input_slots = 2

    def __init__(self, real_object: UsableObject):
        super().__init__(real_object)
        self.blueprints = {frozenset((CopperCable, WoodenPlate)): ElectricCircuit,
                           frozenset((CopperCable, SteelPlate)): Resistor}

    def process(self):
        # todo
        pass


class BurnerElectricGenerator(BurnerMachine):
    input_slots = 1

    def __init__(self, real_object: UsableObject):
        super().__init__(real_object)


class Furnace(BurnerMachine):
    input_slots = 1

    def __init__(self, real_object: UsableObject):
        super().__init__(real_object)
        self.blueprints = {frozenset((Iron,)): IronPlates}
