from core.virtual_objects.materials.intermediates import *
from core.virtual_objects.materials.abstracts import *
from core.virtual_objects.materials.raw_and_basics import *


#
# basic_assembling_blueprints = {frozenset([1, 2]): 3, frozenset([1, 3]): 4}
#
# print(basic_assembling_blueprints[frozenset((3, 1))])


# class Furnace:
#     target: type
#
#     def __init__(self):
#         self.input = Container()
#         self.output = Container()
#         self.performance = 0.5
#         self.progress = 0.0
#
#     def add_target(self, target):
#         self.target = target
#
#     def put(self, batch: MaterialBatch):
#         self.input.add(batch)
#
#     def can_process(self):
#         return self.input.can_produce(batch)
#
#     def process(self):
#         if self.input.can_produce(self.target()):
#             sel


class Player:

    def __init__(self):
        self.bag: Container = Container([CopperCable(15), WoodenPlate(5), Resistor(4)])

    def produce(self, target_batch: ProductMaterial):
        return self.bag.produce_inside(target_batch)


hero = Player()
print(hero.produce(IntegratedCircuit(1)))
print(hero.bag)