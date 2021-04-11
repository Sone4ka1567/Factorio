from base_classes import VirtualObject
from abc import abstractmethod
from core.virtual_objects.container import Container

from collections.abc import Iterable


def flatten(lst):
    for el in lst:
        if isinstance(el, Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el


class MaterialBatch(VirtualObject):
    def __init__(self, amount):
        self.amount = amount

    def __copy__(self):
        return ProductMaterial(self.amount)

    def __str__(self):
        return f'{self.__class__.__name__}: {self.amount}'


class RawMaterial(MaterialBatch):
    def __init__(self, amount, intermediate_class=None):
        super().__init__(amount)
        self.associated_intermediate = intermediate_class

    def __copy__(self):
        return RawMaterial(self.amount, self.associated_intermediate)


class ProductMaterial(MaterialBatch):
    @abstractmethod
    def count_optimal_requirements(self, container: Container):
        pass

    @abstractmethod
    def count_producing_time(self, new_container: Container, producing_time=0):
        pass

    def get_producing_result(self, container: Container):
        container_copy = container.copy()
        requirements = self.count_optimal_requirements(container_copy)
        if not requirements:
            return False
        prod_time = self.count_producing_time(container_copy)
        return container_copy, prod_time


class BasicMaterial(ProductMaterial):
    def __init__(self, amount, raw_class=None):
        super().__init__(amount)
        self.associated_raw = raw_class

    def __copy__(self):
        return BasicMaterial(self.amount, self.associated_raw)

    def count_optimal_requirements(self, container: Container):
        print('need: ', self)
        print('it has: ', container.contains(self))
        print('container:', container)
        if container.contains(self):
            container.remove(self)
            return [self]
        return False

    def count_producing_time(self, new_container: Container, producing_time=0):
        return producing_time


class IntermediateMaterial(ProductMaterial):
    producing_time: float

    def __init__(self, amount, required_res=()):
        super().__init__(amount)
        self.required_res = required_res

    def __copy__(self):
        return IntermediateMaterial(self.amount, self.required_res)

    def count_optimal_requirements(self, container: Container):
        res_set = []
        print('I: need: ', self)
        print('I: it has: ', container.contains(self))
        print('I: container:', container)
        if container.contains(self):
            container.remove(self)
            print('I: ch container:', container)
            return [self]
        for child in self.required_res:
            cur_res = child.count_optimal_requirements(container)
            res_set.append(flatten(cur_res[0]))
        return res_set

    def count_producing_time(self, new_container: Container, producing_time=0):
        if new_container.contains(self):
            return producing_time
        producing_time += self.producing_time * self.amount
        for child in self.required_res:
            producing_time += child.count_producing_time(new_container, producing_time)
        return producing_time
