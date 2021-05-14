import core.virtual_objects.materials.intermediates as inter
import core.virtual_objects.materials.raw_and_basics as rnb
import core.map_objects.production.production as prod
import core.map_objects.production.electricity as el
from core.virtual_objects.map_object_creators.abstract_creators import (
    MapObjectCreator
)


class BurnerFurnaceCreator(MapObjectCreator):
    ticks_to_produce = 10
    producing_time = 0.5

    def __init__(self, amount, map_obj):
        super().__init__(prod.BurnerFurnace, amount, map_obj)
        self.required_res = (rnb.Stone(5 * amount),)


class ElectricFurnaceCreator(MapObjectCreator):
    ticks_to_produce = 20
    producing_time = 1.0

    def __init__(self, amount, map_obj):
        super().__init__(prod.ElectricFurnace, amount, map_obj)
        self.required_res = (
            BurnerFurnaceCreator(amount, map_obj),
            inter.CopperCable(5 * amount),
        )


class BurnerAssemblingMachineCreator(MapObjectCreator):
    ticks_to_produce = 10
    producing_time = 0.5

    def __init__(self, amount, map_obj):
        super().__init__(prod.BurnerAssemblingMachine, amount, map_obj)
        self.required_res = (
            inter.IronPlate(9 * amount),
            inter.IronGearWheel(5 * amount),
            inter.ElectricCircuit(3 * amount),
        )


class ElectricAssemblingMachineCreator(MapObjectCreator):
    ticks_to_produce = 10
    producing_time = 0.5

    def __init__(self, amount, map_obj):
        super().__init__(prod.ElectricAssemblingMachine, amount, map_obj)
        self.required_res = (
            BurnerAssemblingMachineCreator(amount, map_obj),
            inter.IronGearWheel(5 * amount),
            inter.ElectricCircuit(3 * amount),
            inter.SteelPlate(2 * amount),
        )


class BurnerMiningDrillCreator(MapObjectCreator):
    ticks_to_produce = 20
    producing_time = 1.0

    def __init__(self, amount, map_obj):
        super().__init__(prod.BurnerMiningDrill, amount, map_obj)
        self.required_res = (
            inter.IronPlate(3 * amount),
            inter.IronGearWheel(3 * amount),
            BurnerFurnaceCreator(amount, map_obj),
        )

    def matches_with_cell(self, cell):
        return bool(cell.raw_material_batch and cell.raw_material_batch != 0)


class ElectricMiningDrillCreator(MapObjectCreator):
    ticks_to_produce = 40
    producing_time = 2.0

    def __init__(self, amount, map_obj):
        super().__init__(prod.ElectricMiningDrill, amount, map_obj)
        self.required_res = (
            inter.IronGearWheel(8 * amount),
            inter.ElectricCircuit(3 * amount),
            inter.SteelPlate(10 * amount),
        )


class SmallElectricPoleCreator(MapObjectCreator):
    ticks_to_produce = 10
    producing_time = 0.5

    def __init__(self, amount, map_obj):
        super().__init__(el.SmallElectricPole, amount, map_obj)
        self.required_res = (
            inter.CopperCable(2 * amount),
            rnb.Wood(amount),
        )


class BigElectricPoleCreator(MapObjectCreator):
    ticks_to_produce = 10
    producing_time = 0.5

    def __init__(self, amount, map_obj):
        super().__init__(el.BigElectricPole, amount, map_obj)
        self.required_res = (
            inter.CopperPlate(5 * amount),
            inter.CopperCable(3 * amount),
            inter.IronPlate(amount),
        )


class BurnerElectricGenerator(MapObjectCreator):
    ticks_to_produce = 10
    producing_time = 0.5

    def __init__(self, amount, map_obj):
        super().__init__(el.BurnerElectricGenerator, amount, map_obj)
        self.required_res = (
            inter.Pipe(10 * amount),
            inter.IronGearWheel(12 * amount),
            inter.IronPlate(15 * amount),
        )
