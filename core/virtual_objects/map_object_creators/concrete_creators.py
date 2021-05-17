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
    relative_icon_path = '../../../img/icons/creators/production/stone-furnace.png'
    relative_image_path = '../../../img/entity/stone-furnace.xcf'

    def __init__(self, amount, map_obj):
        super().__init__(prod.BurnerFurnace, amount, map_obj)
        self.required_res = (inter.IronPlate(5 * amount), inter.CopperPlate(amount))


class ElectricFurnaceCreator(MapObjectCreator):
    ticks_to_produce = 20
    producing_time = 1.0
    relative_icon_path = '../../../img/icons/creators/production/electric-furnace.png'
    relative_image_path = '../../../img/entity/electric-furnace.png'

    def __init__(self, amount, map_obj):
        super().__init__(prod.ElectricFurnace, amount, map_obj)
        self.required_res = (
            BurnerFurnaceCreator(amount, map_obj),
            inter.CopperCable(5 * amount),
        )


class BurnerAssemblingMachineCreator(MapObjectCreator):
    ticks_to_produce = 10
    producing_time = 0.5
    relative_icon_path = '../../../img/icons/creators/production/assembling-machine-1.png'
    relative_image_path = '../../../img/entity/assembling-machine-1.png'

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
    relative_icon_path = '../../../img/icons/creators/production/assembling-machine-2.png'
    relative_image_path = '../../../img/entity/assembling-machine-2.png'

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
    relative_icon_path = '../../../img/icons/creators/production/burner-mining-drill.png'
    relative_image_path = '../../../img/entity/burner-mining-drill.xcf'

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
    relative_icon_path = '../../../img/icons/creators/production/electric-mining-drill.png'
    relative_image_path = '../../../img/entity/electric-mining-drill.png'

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
    relative_icon_path = '../../../img/icons/creators/electricity/small-electric-pole.png'
    relative_image_path = '../../../img/entity/small-electric-pole.png'

    def __init__(self, amount, map_obj):
        super().__init__(el.SmallElectricPole, amount, map_obj)
        self.required_res = (
            inter.CopperCable(2 * amount),
        )


class BigElectricPoleCreator(MapObjectCreator):
    ticks_to_produce = 10
    producing_time = 0.5
    relative_icon_path = '../../../img/icons/creators/electricity/big-electric-pole.png'
    relative_image_path = '../../../img/entity/big-electric-pole.png'

    def __init__(self, amount, map_obj):
        super().__init__(el.BigElectricPole, amount, map_obj)
        self.required_res = (
            inter.CopperPlate(5 * amount),
            inter.CopperCable(3 * amount),
            inter.IronPlate(amount),
        )


class BurnerElectricGeneratorCreator(MapObjectCreator):
    ticks_to_produce = 10
    producing_time = 0.5
    relative_icon_path = '../../../img/icons/creators/electricity/burner-generator.xcf'
    relative_image_path = '../../../img/entity/burner-generator.png'

    def __init__(self, amount, map_obj):
        super().__init__(el.BurnerElectricGenerator, amount, map_obj)
        self.required_res = (
            inter.Pipe(10 * amount),
            inter.IronGearWheel(12 * amount),
            inter.IronPlate(15 * amount),
        )


class RadarCreator(MapObjectCreator):
    ticks_to_produce = 140
    producing_time = 6.0
    relative_icon_path = '../../../img/icons/radar.png'
    relative_image_path = '../../../img/entity/radar.png'

    def __init__(self, amount, map_obj):
        super().__init__(prod.Radar, amount, map_obj)
        self.required_res = (
            inter.ControlUnit(amount * 3),
            inter.SteelPlate(amount * 25),
            inter.IronGearWheel(amount * 15),
        )


obj2creator = {prod.BurnerFurnace: BurnerFurnaceCreator, prod.ElectricFurnace: ElectricFurnaceCreator,
               prod.BurnerAssemblingMachine: BurnerAssemblingMachineCreator,
               prod.ElectricAssemblingMachine: ElectricAssemblingMachineCreator,
               prod.BurnerMiningDrill: BurnerMiningDrillCreator, prod.ElectricMiningDrill: ElectricMiningDrillCreator,
               el.SmallElectricPole: SmallElectricPoleCreator, el.BigElectricPole: BigElectricPoleCreator,
               el.BurnerElectricGenerator: BurnerElectricGeneratorCreator}
