from core.virtual_objects.materials.material_batch import MaterialBatch
from core.virtual_objects.container import Container


class RawMaterialBatch(MaterialBatch):
    def __init__(self, amount, intermediate_class=None):
        super().__init__(amount)
        self.associated_intermediate = intermediate_class

    def __copy__(self):
        return RawMaterialBatch(self.amount, self.associated_intermediate)

    def count_optimal_requirements(self, container: Container):
        return tuple(self.associated_intermediate(self.amount))


class BasicMaterialBatch(MaterialBatch):
    def __init__(self, amount, raw_class=None):
        super().__init__(amount)
        self.associated_raw = raw_class

    def __copy__(self):
        return BasicMaterialBatch(self.amount, self.associated_raw)

    def count_optimal_requirements(self, container: Container):
        container_copy = container.copy()
        if container_copy.contains(self):
            container_copy.remove(self)
            return [self]
        return False


class IronBatch(RawMaterialBatch):
    def __init__(self, amount):
        super().__init__(amount)
        self.associated_intermediate = IronPlatesBatch


class IronPlatesBatch(BasicMaterialBatch):
    def __init__(self, amount):
        super().__init__(amount)
        self.associated_raw = IronBatch


class CopperBatch(RawMaterialBatch):
    def __init__(self, amount):
        super().__init__(amount)
        self.associated_intermediate = CopperPlatesBatch


class CopperPlatesBatch(BasicMaterialBatch):
    def __init__(self, amount):
        super().__init__(amount)
        self.associated_raw = CopperBatch


class CoalBatch(RawMaterialBatch):
    pass


class StoneBatch(RawMaterialBatch):
    def __init__(self, amount):
        super().__init__(amount)
        self.associated_intermediate = StoneBricksBatch


class StoneBricksBatch(BasicMaterialBatch):
    def __init__(self, amount):
        super().__init__(amount)
        self.associated_raw = StoneBatch


class SiliconBatch(RawMaterialBatch):
    def __init__(self, amount=int(1e5)):
        super().__init__(amount)
        self.associated_intermediate = SiliconPlateBatch


class SiliconPlateBatch(BasicMaterialBatch):
    def __init__(self, amount):
        super().__init__(amount)
        self.associated_raw = SiliconBatch


class WoodBatch(RawMaterialBatch):
    def __init__(self, amount):
        super().__init__(amount)
        self.associated_intermediate = None  # ??????????????


class WoodenPlateBatch(BasicMaterialBatch):
    def __init__(self, amount):
        super().__init__(amount)
        self.associated_raw = WoodBatch

# def exchange(input_batch: RawMaterialBatch, output_batch: RawMaterialBatch, amount: int):
#     if not isinstance(output_batch, type(input_batch)):
#         return False
#     else:
#         possible_amount = min(input_batch.amount, amount)
#         input_batch.amount -= possible_amount
#         output_batch.amount += possible_amount
#         return True
