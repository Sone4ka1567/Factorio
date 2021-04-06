from base_classes import VirtualObject


class MaterialBatch(VirtualObject):
    def __init__(self, amount):
        self.amount = amount

    def __copy__(self):
        return MaterialBatch(self.amount)



class RawMaterialBatch(MaterialBatch):
    def __init__(self, amount, intermediate_class=None):
        super().__init__(amount)
        self.intermediate_class = intermediate_class

    def __copy__(self):
        return RawMaterialBatch(self.amount, self.intermediate_class)


class IronPlatesBatch(MaterialBatch):
    pass


class IronBatch(RawMaterialBatch):
    def __init__(self, amount):
        super().__init__(amount)
        self.intermediate_class = IronPlatesBatch

    def __name__(self):
        return 'IronBatch'

class CopperPlatesBatch(MaterialBatch):
    pass


class CopperBatch(RawMaterialBatch):
    def __init__(self, amount):
        super().__init__(amount)
        self.intermediate_class = CopperPlatesBatch
    def __name__(self):
        return 'CopperBatch'

class CoalBatch(RawMaterialBatch):
    def __init__(self, amount):
        super().__init__(amount)
        self.intermediate_class = None  # ??????????????
    def __name__(self):
        return 'CoalBatch'

class StoneBricksBatch(MaterialBatch):
    pass


class StoneBatch(RawMaterialBatch):
    def __init__(self, amount):
        super().__init__(amount)
        self.intermediate_class = StoneBricksBatch
    def __name__(self):
        return 'StoneBatch'

class TreeBatch(RawMaterialBatch):
    def __init__(self, amount):
        super().__init__(amount)
        self.intermediate_class = None  # ??????????????
    def __name__(self):
        return 'TreeBatch'
# def exchange(input_batch: RawMaterialBatch, output_batch: RawMaterialBatch, amount: int):
#     if not isinstance(output_batch, type(input_batch)):
#         return False
#     else:
#         possible_amount = min(input_batch.amount, amount)
#         input_batch.amount -= possible_amount
#         output_batch.amount += possible_amount
#         return True
