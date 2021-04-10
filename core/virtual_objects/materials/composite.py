from intermediates import *
from material_batch import *
from raw_and_basics import *
from abc import ABC, abstractmethod
from typing import List
from abc import ABC, abstractmethod


class Bag:
    def __init__(self):
        self.data = []

    def contains(self, batch):
        for cur_batch in self.data:
            if isinstance(cur_batch, type(batch)):
                return cur_batch.amount >= batch.amount
        return False

    def add(self, batch):
        for idx, cur_batch in enumerate(self.data):
            if isinstance(cur_batch, type(batch)):
                self.data[idx].amount += batch.amount

    def remove(self, batch):
        for idx, cur_batch in enumerate(self.data):
            if isinstance(cur_batch, type(batch)):
                if cur_batch > batch.amount:
                    self.data[idx].amount -= batch.amount
                else:
                    self.data[idx] = None

    def get_data(self):
        return self.data


def produce_manually(batch: MaterialBatch):
    pass


class Component(ABC):
    def __init__(self, bag: Bag):
        self.bag = bag

    # @property
    # def parent(self):
    #     return self._parent
    #
    # @parent.setter
    # def parent(self, parent):
    #     self._parent = parent

    @abstractmethod
    def count_requirements(self, required_batch):
        pass


class Leaf(Component):
    def count_requirements(self, required_batch: BasicMaterialBatch):
        if self.bag.contains(required_batch):
            self.bag.remove(required_batch)
            return required_batch
        return False


class Composite(Component):
    def __init__(self, bag: Bag):
        super().__init__(bag)
        self._children =

    def count_requirements(self, bag: Bag):
        res_set = []
        for child in self._children:
            cur_res = child.count_requirements()
            if not cur_res:
                return False
            res_set.append(cur_res)
        return res_set
