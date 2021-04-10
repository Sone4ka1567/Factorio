from core.virtual_objects.materials.material_batch import MaterialBatch
from core.virtual_objects.materials.raw_and_basics import (
    CopperPlatesBatch,
    IronPlatesBatch,
    WoodenPlateBatch,
    SiliconPlateBatch,
)
from core.virtual_objects.container import Container


class IntermediateMaterialBatch(MaterialBatch):
    def __init__(self, amount, required_res=()):
        super().__init__(amount)
        self.required_res = required_res

    def __copy__(self):
        return IntermediateMaterialBatch(self.amount, self.required_res)

    def count_optimal_requirements(self, container: Container):
        container_copy = container.copy()
        res_set = []
        if container_copy.contains(self):
            container_copy.remove(self)
            return [self]
        for child in self.required_res:
            cur_res = child.count_optimal_requirements(container_copy)
            if not cur_res:
                return False
            res_set.append(*cur_res)
        return res_set


class CopperCable(IntermediateMaterialBatch):
    def __init__(self, amount):
        super().__init__(amount)
        self.required_res = (CopperPlatesBatch(max(amount // 2, 1)),)


class SteelPlate(IntermediateMaterialBatch):
    def __init__(self, amount):
        super().__init__(amount)
        self.required_res = (IronPlatesBatch(amount),)


class Pipe(IntermediateMaterialBatch):
    def __init__(self, amount):
        super().__init__(amount)
        self.required_res = (IronPlatesBatch(amount),)


class IronGearWheel(IntermediateMaterialBatch):
    def __init__(self, amount):
        super().__init__(amount)
        self.required_res = (IronPlatesBatch(amount * 2),)


class ElectricCircuit(IntermediateMaterialBatch):
    def __init__(self, amount):
        super().__init__(amount)
        self.required_res = (CopperCable(amount * 3), WoodenPlateBatch(amount))


class Resistor(IntermediateMaterialBatch):
    def __init__(self, amount):
        super().__init__(amount)
        self.required_res = (CopperCable(amount * 2), SteelPlate(amount))


class Transistor(IntermediateMaterialBatch):
    def __init__(self, amount):
        super().__init__(amount)
        self.required_res = (SiliconPlateBatch(amount * 3), IronPlatesBatch(amount))


class IntegratedCircuit(IntermediateMaterialBatch):
    def __init__(self, amount):
        super().__init__(amount)
        self.required_res = (ElectricCircuit(amount * 5), Resistor(amount * 3))


class ControlUnit(IntermediateMaterialBatch):
    def __init__(self, amount):
        super().__init__(amount)
        self.required_res = (IntegratedCircuit(amount * 5), Transistor(amount * 5))


class Radar(IntermediateMaterialBatch):
    def __init__(self, amount):
        super().__init__(amount)
        self.required_res = (
            ControlUnit(amount * 3),
            SteelPlate(amount * 25),
            IronGearWheel(amount * 15),
        )


if __name__ == "__main__":
    batch = Resistor(2)
    real_bag = Container([IronPlatesBatch(3), CopperPlatesBatch(2)])
    res = batch.count_optimal_requirements(real_bag)
    for _ in res:
        print(_)
