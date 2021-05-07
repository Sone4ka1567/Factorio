import core.virtual_objects.materials.intermediates as inter
import core.virtual_objects.materials.raw_and_basics as rnb
import core.map_objects.production.production as prod
import core.map_objects.production.electricity as el
from core.virtual_objects.map_object_creators.abstract_creators import (
    MachineCreator,
    DrillCreator,
    ElectricPoleCreator,
    GeneratorCreator,
)


# MACHINE CREATORS


class BurnerFurnaceCreator(MachineCreator):
    ticks_to_produce = 10
    producing_time = 0.5

    def __init__(self, amount):
        super().__init__(prod.BurnerFurnace, amount)
        self.required_res = (rnb.Stone(5 * amount),)


class ElectricFurnaceCreator(MachineCreator):
    ticks_to_produce = 20
    producing_time = 1.0

    def __init__(self, amount):
        super().__init__(prod.ElectricFurnace, amount)
        self.required_res = (
            BurnerFurnaceCreator(amount),
            inter.CopperCable(5 * amount),
        )


class BurnerAssemblingMachineCreator(MachineCreator):
    ticks_to_produce = 10
    producing_time = 0.5

    def __init__(self, amount):
        super().__init__(prod.BurnerAssemblingMachine, amount)
        self.required_res = (
            inter.IronPlates(9 * amount),
            inter.IronGearWheel(5 * amount),
            inter.ElectricCircuit(3 * amount),
        )


class ElectricAssemblingMachineCreator(MachineCreator):
    ticks_to_produce = 10
    producing_time = 0.5

    def __init__(self, amount):
        super().__init__(prod.ElectricAssemblingMachine, amount)
        self.required_res = (
            BurnerAssemblingMachineCreator(amount),
            inter.IronGearWheel(5 * amount),
            inter.ElectricCircuit(3 * amount),
            inter.SteelPlate(2 * amount),
        )


# DRILL CREATORS


class BurnerMiningDrillCreator(DrillCreator):
    ticks_to_produce = 20
    producing_time = 1.0

    def __init__(self, amount):
        super().__init__(prod.BurnerMiningDrill, amount)
        self.required_res = (
            inter.IronPlates(3 * amount),
            inter.IronGearWheel(3 * amount),
            BurnerFurnaceCreator(amount),
        )


class ElectricMiningDrillCreator(DrillCreator):
    ticks_to_produce = 40
    producing_time = 2.0

    def __init__(self, amount):
        super().__init__(prod.ElectricMiningDrill, amount)
        self.required_res = (
            inter.IronGearWheel(8 * amount),
            inter.ElectricCircuit(3 * amount),
            inter.SteelPlate(10 * amount),
        )


# POLE CREATORS


class SmallElectricPoleCreator(ElectricPoleCreator):
    ticks_to_produce = 10
    producing_time = 0.5

    def __init__(self, amount):
        super().__init__(el.SmallElectricPole, amount)
        self.required_res = (
            inter.CopperCable(2 * amount),
            rnb.Wood(amount),
        )


class BigElectricPoleCreator(ElectricPoleCreator):
    ticks_to_produce = 10
    producing_time = 0.5

    def __init__(self, amount):
        super().__init__(el.BigElectricPole, amount)
        self.required_res = (
            inter.CopperPlates(5 * amount),
            inter.CopperCable(3 * amount),
            inter.IronPlates(amount),
        )


# GENERATOR CREATORS


class BurnerElectricGenerator(GeneratorCreator):
    ticks_to_produce = 10
    producing_time = 0.5

    def __init__(self, amount):
        super().__init__(el.BigElectricPole, amount)
        self.required_res = (
            inter.Pipe(10 * amount),
            inter.IronGearWheel(12 * amount),
            inter.IronPlates(15 * amount),
        )
