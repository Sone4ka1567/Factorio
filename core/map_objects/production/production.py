from abc import ABC

from core.virtual_objects.materials.raw_and_basics import RawMaterial, Iron, Copper, Silicon
import core.virtual_objects.materials.intermediates as inter
from core.map_objects.production.power_source import (
    ElectricPowerSource,
    BurnerPowerSource,
)
from core.map_objects.production.machine import Machine


class Furnace(Machine, ABC):
    input_slots_num = 1
    energy_consumption: int

    def __init__(self, x, y, map_obj):
        super().__init__(x, y, map_obj)
        self.progress = 0
        self.target_type = None

    def process(self):
        if not self.energy_source.has_energy():
            return
        self.energy_source.subtract_energy(self.progress)
        if self.progress == 0:
            if self.input.is_empty():
                return
            input_batch = self.input[0]
            self.target_type = input_batch.associated_basic
            self.ticks_per_batch = self.target_type.ticks_to_produce // self.speed
            self.input.remove(input_batch.get_n(1))
            self.progress += 1
        else:
            if self.progress == self.ticks_per_batch:
                putting_res = self.output.put(self.target_type(1))
                if not putting_res:
                    print("CANNOT PUT RES")
                    return
                self.progress = 0
            else:
                self.progress += 1


class AssemblingMachine(Machine, ABC):
    input_slots_num = 1
    possible_targets: list

    def __init__(self, x, y, map_obj):
        super().__init__(x, y, map_obj)
        self.progress = 0
        self.target_type = None

    def set_target(self, target: type):
        if target in self.possible_targets:
            self.target_type = target
            return True
        return False

    def process(self):
        if not self.energy_source.has_energy():
            return
        self.energy_source.subtract_energy(self.progress)
        if self.progress == 0:
            if self.input.is_empty() or not self.target_type:
                return
            self.ticks_per_batch = self.target_type.ticks_to_produce // self.speed
            requirements = self.target_type(1).required_res
            for r in requirements:
                if not self.input.contains(r):
                    return
                self.input.remove(r)
            self.progress += 1
        elif self.progress == self.ticks_per_batch:
            putting_res = self.output.put(self.target_type(1))
            if not putting_res:
                print("CANNOT PUT RES")
                return
            self.progress = 0
        else:
            self.progress += 1


class MiningDrill(Machine, ABC):
    input_slots_num = 0

    def __init__(self, x, y, map_obj):
        super().__init__(x, y, map_obj)
        self.cell = map_obj.get_cell(x, y)

    def process(self):
        if not self.energy_source.has_energy():
            return
        self.ticks_per_batch = RawMaterial.ticks_to_produce // self.speed
        if not self.cell.raw_material_batch:
            return
        if self.cell.raw_material_batch.amount >= 1:
            self.cell.raw_material_batch -= 1
            self.output.put(self.cell.raw_material_batch.get_n(1))
            self.energy_source.subtract_energy()
        if self.cell.raw_material_batch and self.cell.raw_material_batch.amount == 0:
            self.cell.raw_material_batch = None


class BurnerFurnace(Furnace):
    valid_input = (Iron, Copper, Silicon)
    energy_consumption = 1
    speed = 1

    def __init__(self, x, y, map_obj):
        super().__init__(x, y, map_obj)
        self.energy_source = BurnerPowerSource(self.energy_consumption)


class ElectricFurnace(Furnace):
    valid_input = BurnerFurnace.valid_input
    energy_consumption = 50
    speed = 2

    def __init__(self, x, y, map_obj):
        super().__init__(x, y, map_obj)
        self.energy_source = ElectricPowerSource(self.energy_consumption)


class BurnerAssemblingMachine(AssemblingMachine):
    valid_input = (inter.IronPlate, inter.CopperPlate, inter.WoodenPlate)
    possible_targets = (inter.CopperCable, inter.SteelPlate, inter.Pipe, inter.IronGearWheel)
    energy_consumption = 1
    speed = 1

    def __init__(self, x, y, map_obj):
        super().__init__(x, y, map_obj)
        self.energy_source = BurnerPowerSource(self.energy_consumption)


class ElectricAssemblingMachine(AssemblingMachine):
    valid_input = (
            BurnerAssemblingMachine.valid_input
            + (inter.SiliconPlate,)
            + BurnerAssemblingMachine.possible_targets
    )
    possible_targets = BurnerAssemblingMachine.possible_targets + (
        inter.ElectricCircuit,
        inter.Resistor,
        inter.Transistor,
        inter.IntegratedCircuit,
        inter.ControlUnit,
    )
    energy_consumption = 40
    speed = 2

    def __init__(self, x, y, map_obj):
        super().__init__(x, y, map_obj)
        self.energy_source = ElectricPowerSource(self.energy_consumption)


class BurnerMiningDrill(MiningDrill):
    energy_consumption = 1
    speed = 1

    def __init__(self, x, y, map_obj):
        super().__init__(x, y, map_obj)
        self.energy_source = BurnerPowerSource(self.energy_consumption)


class ElectricMiningDrill(MiningDrill):
    energy_consumption = 50
    speed = 2

    def __init__(self, x, y, map_obj):
        super().__init__(x, y, map_obj)
        self.energy_source = ElectricPowerSource(self.energy_consumption)


class Radar(Machine):
    def process(self):
        pass
