from abc import abstractmethod
from collections.abc import Iterable
from base_classes import VirtualObject
from core.container import Container


def flatten(lst):
    for element in lst:
        if isinstance(element, Iterable) and not isinstance(element, (str, bytes)):
            yield from flatten(element)
        else:
            yield element


class MaterialBatch(VirtualObject):
    def __init__(self, amount):
        self.amount = amount

    def __str__(self):
        return f"{self.__class__.__name__}: {self.amount}"

    @staticmethod
    def get_n(n):
        return MaterialBatch(n)


class RawMaterial(MaterialBatch):
    def __init__(self, amount, intermediate_class=None):
        super().__init__(amount)
        self.associated_intermediate = intermediate_class

    def copy(self):
        return RawMaterial(self.amount, self.associated_intermediate)


class ProductMaterial(MaterialBatch):
    producing_time: float
    ticks_to_produce: int

    # def ticks_to_produce(self):
    #     return int(self.producing_time * 2)  # КОСТЫЛЬ

    @abstractmethod
    def count_optimal_requirements(self, container: Container):
        pass

    @abstractmethod
    def count_producing_time(self, container: Container, producing_time=0):
        pass

    def get_producing_result(self, container: Container):
        container_copy = container.copy()
        requirements = self.count_optimal_requirements(container_copy)
        if not requirements:
            return False
        prod_time = self.count_producing_time(container)
        return container_copy, prod_time


class BasicMaterial(ProductMaterial):
    def __init__(self, amount, raw_class=None):
        super().__init__(amount)
        self.associated_raw = raw_class

    def copy(self):
        return BasicMaterial(self.amount, self.associated_raw)

    def count_optimal_requirements(self, container: Container):
        print("-" * 20)
        print("B: need: ", self)
        print("B: it has: ", container.contains(self))
        if container.contains(self):
            container.remove(self)
            return [self]
        return False

    def count_producing_time(self, container: Container, producing_time=0):
        return 0


class IntermediateMaterial(ProductMaterial):

    def __init__(self, amount, required_res=()):
        super().__init__(amount)
        self.required_res = required_res

    def copy(self):
        return IntermediateMaterial(self.amount, self.required_res)

    def count_optimal_requirements(self, container: Container):
        res_set = []
        print("-" * 20)
        print("I: need: ", self)
        print("I: it has: ", container.contains(self))
        if container.contains(self):
            container.remove(self)
            print("I: ch container:", container)
            return [self]
        for child in self.required_res:
            cur_res = child.count_optimal_requirements(container)
            if cur_res:
                res_set.append(flatten(cur_res[0]))
            else:
                return False
        return res_set

    def count_producing_time(self, container: Container, producing_time=0):
        if container.contains(self):
            return 0
        producing_time = self.producing_time * self.amount
        for child in self.required_res:
            producing_time += child.count_producing_time(container, producing_time)
        return producing_time
