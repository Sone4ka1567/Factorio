from core.virtual_objects.materials.abstracts import Intermediate
from core.virtual_objects.materials.raw_and_basics import (
    CopperPlate,
    IronPlate,
    SiliconPlate,
)


class CopperCable(Intermediate):
    ticks_to_produce = 10
    producing_time = 0.5
    relative_icon_path = '../../../img/icons/materials/intermediate/copper-cable.png'

    def __init__(self, amount):
        super().__init__(amount)
        self.required_res = (CopperPlate(max(amount // 2, 1)),)


class SteelPlate(Intermediate):
    ticks_to_produce = 20
    producing_time = 1.0
    relative_icon_path = '../../../img/icons/materials/intermediate/steel-plate.png'

    def __init__(self, amount):
        super().__init__(amount)
        self.required_res = (IronPlate(amount),)


class Pipe(Intermediate):
    ticks_to_produce = 20
    producing_time = 1.0
    relative_icon_path = '../../../img/icons/materials/intermediate/pipe.png'

    def __init__(self, amount):
        super().__init__(amount)
        self.required_res = (IronPlate(amount),)


class IronGearWheel(Intermediate):
    ticks_to_produce = 40
    producing_time = 2.0
    relative_icon_path = '../../../img/icons/materials/intermediate/iron-gear-wheel.png'

    def __init__(self, amount):
        super().__init__(amount)
        self.required_res = (IronPlate(amount * 2),)


class ElectricCircuit(Intermediate):
    ticks_to_produce = 10
    producing_time = 0.5
    relative_icon_path = '../../../img/icons/materials/intermediate/electric-circuit.png'

    def __init__(self, amount):
        super().__init__(amount)
        self.required_res = (CopperCable(amount * 3),)


class Resistor(Intermediate):
    ticks_to_produce = 20
    producing_time = 1.0
    relative_icon_path = '../../../img/icons/materials/intermediate/resistor.xcf'

    def __init__(self, amount):
        super().__init__(amount)
        self.producing_time = 1.0
        self.required_res = (CopperCable(amount * 2), SteelPlate(amount))


class Transistor(Intermediate):
    ticks_to_produce = 40
    producing_time = 2.0
    relative_icon_path = '../../../img/icons/materials/intermediate/transistor.xcf'

    def __init__(self, amount):
        super().__init__(amount)
        self.required_res = (SiliconPlate(amount * 3), IronPlate(amount))


class IntegratedCircuit(Intermediate):
    ticks_to_produce = 60
    producing_time = 3.0
    relative_icon_path = '../../../img/icons/materials/intermediate/integrated-circuit.png'

    def __init__(self, amount):
        super().__init__(amount)
        self.required_res = (ElectricCircuit(amount * 5), Resistor(amount * 3))


class ControlUnit(Intermediate):
    ticks_to_produce = 100
    producing_time = 5.0
    relative_icon_path = '../../../img/icons/materials/intermediate/control-unit.png'

    def __init__(self, amount):
        super().__init__(amount)
        self.required_res = (IntegratedCircuit(amount * 5), Transistor(amount * 5))
