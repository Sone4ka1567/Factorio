from material_batch import MaterialBatch
from raw_and_basics import CopperPlatesBatch, IronPlatesBatch, BasicMaterialBatch, IronBatch
from abc import ABC, abstractmethod
from core.virtual_objects.container import Container


class IntermediateMaterialBatch(MaterialBatch):
    def __init__(self, amount, required_res=()):
        super().__init__(amount)
        self.required_res = required_res

    def __copy__(self):
        return IntermediateMaterialBatch(self.amount, self.required_res)

    def count_requirements(self, container: Container):
        res_set = []
        for child in self.required_res:
            cur_res = child.count_requirements(container)
            if not cur_res:
                return False
            res_set.append(cur_res)
        return res_set


class CopperCable(IntermediateMaterialBatch):
    def __init__(self, amount):
        super().__init__(amount)
        self.required_res = (CopperPlatesBatch(max(amount // 2, 1)),)


class SteelPlate(IntermediateMaterialBatch):
    def __init__(self, amount):
        super().__init__(amount)
        self.required_res = (IronPlatesBatch(amount),)


class Resistor(IntermediateMaterialBatch):
    def __init__(self, amount):
        super().__init__(amount)
        self.required_res = (CopperCable(2 * amount), SteelPlate(amount))  # CONST


if __name__ == '__main__':
    batch = Resistor(2)
    real_bag = Container([IronPlatesBatch(3), CopperPlatesBatch(2)])
    bag_copy = real_bag.copy()
    print(batch.count_requirements(bag_copy))
    print(bag_copy)
    print(real_bag)
