from core.virtual_objects.materials.abstracts import RawMaterial, BasicMaterial


class Iron(RawMaterial):
    icon_path = '../../../img/icons/materials/raw/iron-ore.png'

    def __init__(self, amount):
        super().__init__(amount)
        self.associated_basic = IronPlate


class IronPlate(BasicMaterial):
    ticks_to_produce = 10
    producing_time = 0.5
    icon_path = '../../../img/icons/materials/basic/iron-plate.png'

    def __init__(self, amount):
        super().__init__(amount)
        self.associated_raw = Iron


class Copper(RawMaterial):
    icon_path = '../../../img/icons/materials/raw/copper-ore.png'

    def __init__(self, amount):
        super().__init__(amount)
        self.associated_basic = CopperPlate


class CopperPlate(BasicMaterial):
    ticks_to_produce = 10
    producing_time = 0.5
    icon_path = '../../../img/icons/materials/basic/copper-plate.png'

    def __init__(self, amount):
        super().__init__(amount)
        self.associated_raw = Copper


class Coal(RawMaterial):
    icon_path = '../../../img/icons/materials/raw/coal.png'

    @staticmethod
    def is_fuel():
        return True


class Stone(RawMaterial):
    icon_path = '../../../img/icons/materials/raw/stone.png'

    def __init__(self, amount):
        super().__init__(amount)
        self.associated_basic = StoneBricks


class StoneBricks(BasicMaterial):
    ticks_to_produce = 10
    producing_time = 0.5
    icon_path = '../../../img/icons/materials/basic/stone-brick.png'

    def __init__(self, amount):
        super().__init__(amount)
        self.associated_raw = Stone


class Silicon(RawMaterial):
    icon_path = '../../../img/icons/materials/raw/silicon.png'

    def __init__(self, amount=int(1e5)):
        super().__init__(amount)
        self.associated_basic = SiliconPlate


class SiliconPlate(BasicMaterial):
    ticks_to_produce = 15
    producing_time = 0.5
    icon_path = '../../../img/icons/materials/basic/silicon-plate.png'

    def __init__(self, amount):
        super().__init__(amount)
        self.associated_raw = Silicon


class Wood(RawMaterial):
    icon_path = '../../../img/icons/materials/raw/wood.png'


class WoodenPlate(BasicMaterial):
    ticks_to_produce = 10
    producing_time = 0.5
    icon_path = '../../../img/icons/materials/basic/wooden-plate.xcf'

    def __init__(self, amount):
        super().__init__(amount)
        self.associated_raw = Wood
