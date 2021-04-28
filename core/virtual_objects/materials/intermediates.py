from core.virtual_objects.materials.abstracts import IntermediateMaterial
from core.virtual_objects.materials.raw_and_basics import (
    CopperPlates,
    IronPlates,
    WoodenPlate,
    SiliconPlate,
)


class CopperCable(IntermediateMaterial):
    ticks_to_produce = 1
    producing_time = 0.5

    def __init__(self, amount):
        super().__init__(amount)
        self.required_res = (CopperPlates(max(amount // 2, 1)),)


class SteelPlate(IntermediateMaterial):
    ticks_to_produce = 2
    producing_time = 1.0

    def __init__(self, amount):
        super().__init__(amount)
        self.required_res = (IronPlates(amount),)


class Pipe(IntermediateMaterial):
    ticks_to_produce = 2
    producing_time = 1.0

    def __init__(self, amount):
        super().__init__(amount)
        self.required_res = (IronPlates(amount),)


class IronGearWheel(IntermediateMaterial):
    ticks_to_produce = 4
    producing_time = 2.0

    def __init__(self, amount):
        super().__init__(amount)
        self.required_res = (IronPlates(amount * 2),)


class ElectricCircuit(IntermediateMaterial):
    ticks_to_produce = 1
    producing_time = 0.5

    def __init__(self, amount):
        super().__init__(amount)
        self.required_res = (CopperCable(amount * 3), WoodenPlate(amount))


class Resistor(IntermediateMaterial):
    ticks_to_produce = 2
    producing_time = 1.0

    def __init__(self, amount):
        super().__init__(amount)
        self.producing_time = 1.0
        self.required_res = (CopperCable(amount * 2), SteelPlate(amount))


class Transistor(IntermediateMaterial):
    ticks_to_produce = 4
    producing_time = 2.0

    def __init__(self, amount):
        super().__init__(amount)
        self.required_res = (SiliconPlate(amount * 3), IronPlates(amount))


class IntegratedCircuit(IntermediateMaterial):
    ticks_to_produce = 6
    producing_time = 3.0

    def __init__(self, amount):
        super().__init__(amount)
        self.required_res = (ElectricCircuit(amount * 5), Resistor(amount * 3))


class ControlUnit(IntermediateMaterial):
    ticks_to_produce = 10
    producing_time = 5.0

    def __init__(self, amount):
        super().__init__(amount)
        self.required_res = (IntegratedCircuit(amount * 5), Transistor(amount * 5))


class Radar(IntermediateMaterial):
    ticks_to_produce = 14
    producing_time = 6.0

    def __init__(self, amount):
        super().__init__(amount)
        self.required_res = (
            ControlUnit(amount * 3),
            SteelPlate(amount * 25),
            IronGearWheel(amount * 15),
        )
