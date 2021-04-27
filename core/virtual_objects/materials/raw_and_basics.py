from core.virtual_objects.materials.abstracts import RawMaterial, BasicMaterial


class Iron(RawMaterial):
    def __init__(self, amount):
        super().__init__(amount)
        self.associated_basic = IronPlates


class IronPlates(BasicMaterial):
    ticks_to_produce = 1
    producing_time = 0.5

    def __init__(self, amount):
        super().__init__(amount)
        self.associated_raw = Iron


class Copper(RawMaterial):
    def __init__(self, amount):
        super().__init__(amount)
        self.associated_basic = CopperPlates


class CopperPlates(BasicMaterial):
    def __init__(self, amount):
        super().__init__(amount)
        self.producing_time = 0.5
        self.associated_raw = Copper


class Coal(RawMaterial):
    pass


class Stone(RawMaterial):
    def __init__(self, amount):
        super().__init__(amount)
        self.associated_basic = StoneBricks


class StoneBricks(BasicMaterial):
    def __init__(self, amount):
        super().__init__(amount)
        self.producing_time = 0.5
        self.associated_raw = Stone


class Silicon(RawMaterial):
    def __init__(self, amount=int(1e5)):
        super().__init__(amount)
        self.associated_basic = SiliconPlate


class SiliconPlate(BasicMaterial):
    def __init__(self, amount):
        super().__init__(amount)
        self.producing_time = 0.5
        self.associated_raw = Silicon


class Wood(RawMaterial):
    def __init__(self, amount):
        super().__init__(amount)
        self.associated_basic = None  # ??????????????


class WoodenPlate(BasicMaterial):
    def __init__(self, amount):
        super().__init__(amount)
        self.producing_time = 0.5
        self.associated_raw = Wood

# def exchange(input_batch: RawMaterialBatch, output_batch: RawMaterialBatch, amount: int):
#     if not isinstance(output_batch, type(input_batch)):
#         return False
#     else:
#         possible_amount = min(input_batch.amount, amount)
#         input_batch.amount -= possible_amount
#         output_batch.amount += possible_amount
#         return True
