from abc import abstractmethod
from os.path import abspath
from collections.abc import Iterable
from virtual_object import VirtualObject
from core.container import Container


def flatten(lst):
    for element in lst:
        if isinstance(element, Iterable) and not isinstance(element, (str, bytes)):
            yield from flatten(element)
        else:
            yield element


class MaterialBatch(VirtualObject):
    relative_icon_path: str

    def get_icon_path(self):
        return abspath(self.relative_icon_path.replace('../', ''))

    def __str__(self):
        return f"{self.__class__.__name__}: {self.amount}"

    def get_n(self, n):
        return type(self)(n)

    @staticmethod
    def is_fuel():
        return False

    def to_json(self):
        return {"type": self.__class__.__name__, "amount": self.amount}


class RawMaterial(MaterialBatch):
    ticks_to_produce = 10

    def __init__(self, amount, basic_class=None):
        super().__init__(amount)
        self.associated_basic = basic_class

    def copy(self):
        return RawMaterial(self.amount, self.associated_basic)

    def __isub__(self, other):
        self.amount -= min(self.amount, other)
        return self


class ProductMaterial(MaterialBatch):
    producing_time: float
    ticks_to_produce: int

    @abstractmethod
    def count_optimal_requirements(self, container: Container, count=0):
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

    def count_optimal_requirements(self, container: Container, count=0):
        print("-" * 20)
        print("B: need: ", self)
        print("B: it has: ", container.contains(self))
        if container.contains(self):
            container.remove(self)
            return [self]
        return False

    def count_producing_time(self, container: Container, producing_time=0):
        return 0


class Intermediate(ProductMaterial):
    required_res: tuple

    def __init__(self, amount, required_res=()):
        super().__init__(amount)
        self.required_res = required_res

    def copy(self):
        return Intermediate(self.amount, self.required_res)

    def count_optimal_requirements(self, container: Container, count=0):
        res_set = []
        print("-" * 20)
        print("I: need: ", self)
        print("I: it has: ", container.contains(self))
        if container.contains(self) and count != 0:
            container.remove(self)
            print("I: ch container:", container)
            return [self]
        for child in self.required_res:
            cur_res = child.count_optimal_requirements(container, 1)
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
