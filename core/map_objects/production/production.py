from abc import abstractmethod, ABC

from core.map_objects.abstracts import UsableObjectProxy
from core.map_objects.abstracts import UsableObject
from core.container import Container

from core.virtual_objects.materials.raw_and_basics import *
from core.virtual_objects.materials.intermediates import *
from maps import MapCell
from core.map_objects.production.power_source import PowerSource, ElectricPowerSource, BurnerPowerSource


class Machine(ABC):
    input_slots_num: int
    progress = 0
    energy_source: PowerSource
    valid_input: list
    energy_consumption: int
    speed: int
    batches_per_tick: int

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


class Furnace(Machine, ABC):
    input_slots_num = 1
    energy_consumption: int

    def __init__(self):
        super().__init__()
        self.progress = 0
        self.target_type = None
        self.batches_per_tick = 1

    def process(self):
        if not self.energy_source.has_energy():
            return
        if self.progress == 0:
            if self.input.is_empty():
                return
            input_batch = self.input[0]
            self.target_type = input_batch.associated_basic
            self.batches_per_tick = self.speed // self.target_type.ticks_to_produce
            self.input.remove(input_batch.get_n(self.batches_per_tick))
            self.progress += 1
            self.energy_source.subtract_energy()
        else:
            if self.progress == self.target_type.ticks_to_produce:
                putting_res = self.output.put(self.target_type(self.batches_per_tick))
                if not putting_res:
                    print('CANNOT PUT RES')
                    return
                self.progress = 0
            else:
                self.progress += 1
        print(
            f"progress: {self.progress}, input: {self.input}, output: {self.output}, energy: {self.energy_source.amount()}"
        )


class AssemblingMachine(Machine, ABC):
    input_slots_num = 1
    possible_targets: list

    def __init__(self):
        super().__init__()
        self.progress = 0
        self.target_type = None
        self.batches_per_tick = 1

    def set_target(self, target: type):
        if target in self.possible_targets:
            self.target_type = target
            return True
        return False

    def process(self):
        if not self.energy_source.has_energy():
            return
        if self.progress == 0:
            if self.input.is_empty() or not self.target_type:
                return
            self.batches_per_tick = self.speed // self.target_type.ticks_to_produce
            requirements = self.target_type(self.batches_per_tick).required_res
            for r in requirements:
                if not self.input.contains(r):
                    return
                self.input.remove(r)
            self.energy_source.subtract_energy()
            self.progress += 1
        elif self.progress == self.target_type.ticks_to_produce:
            putting_res = self.output.put(self.target_type(self.batches_per_tick))
            if not putting_res:
                print('CANNOT PUT RES')
                return
            self.progress = 0
        else:
            self.progress += 1
        # print(
        #     f"progress: {self.progress}, input: {self.input}, output: {self.output}, energy: {self.energy_source.amount()}"
        # )


class MiningDrill(Machine, ABC):
    input_slots_num = 0

    def __init__(self, cell: MapCell):
        super().__init__()
        self.cell = cell
        self.batches_per_tick = 1

    def process(self):
        if not self.energy_source.has_energy():
            return
        self.batches_per_tick = self.speed // RawMaterial.ticks_to_produce
        if self.cell.raw_material_batch.amount >= self.batches_per_tick:
            self.cell.raw_material_batch -= self.batches_per_tick
            self.output.put(self.cell.raw_material_batch.get_n(self.batches_per_tick))
            self.energy_source.subtract_energy()
        if self.cell.raw_material_batch and self.cell.raw_material_batch.amount == 0:
            self.cell.raw_material_batch = None


class BurnerFurnace(Furnace):
    valid_input = [Coal, Iron]
    energy_consumption = 1
    speed = 1

    def __init__(self):
        super().__init__()
        self.energy_source = BurnerPowerSource(self.energy_consumption)


class ElectricFurnace(Furnace):
    valid_input = [Iron]
    energy_consumption = 50
    speed = 2

    def __init__(self):
        super().__init__()
        self.energy_source = ElectricPowerSource(self.energy_consumption)


class BurnerAssemblingMachine(AssemblingMachine):
    valid_input = (IronPlates, CopperPlates, WoodenPlate)
    possible_targets = (CopperCable, SteelPlate, Pipe, IronGearWheel)
    energy_consumption = 1
    speed = 1

    def __init__(self):
        super().__init__()
        self.energy_source = BurnerPowerSource(self.energy_consumption)


class ElectricAssemblingMachine(AssemblingMachine):
    valid_input = BurnerAssemblingMachine.valid_input + (SiliconPlate,) + BurnerAssemblingMachine.possible_targets
    possible_targets = BurnerAssemblingMachine.possible_targets + (
        ElectricCircuit, Resistor, Transistor, IntegratedCircuit, ControlUnit)
    energy_consumption = 40
    speed = 1

    def __init__(self):
        super().__init__()
        self.energy_source = ElectricPowerSource(self.energy_consumption)


class BurnerMiningDrill(MiningDrill):
    energy_consumption = 1
    speed = 1

    def __init__(self, cell: MapCell):
        super().__init__(cell)
        self.energy_source = BurnerPowerSource(self.energy_consumption)


class ElectricMiningDrill(MiningDrill):
    energy_consumption = 50
    speed = 2

    def __init__(self, cell: MapCell):
        super().__init__(cell)
        self.energy_source = ElectricPowerSource(self.energy_consumption)