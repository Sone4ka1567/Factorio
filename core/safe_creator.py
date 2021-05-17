from abc import ABC, abstractmethod
from result_func import result_ok, result_error


class Handler(ABC):
    @abstractmethod
    def set_next(self, h):
        pass

    @abstractmethod
    def handle(self, object_creator, x, y):
        pass


class AbstractHandler(Handler, ABC):
    def __init__(self, map_obj):
        self.next: Handler = None
        self.map_obj = map_obj

    def set_next(self, h):
        self.next = h
        return h

    def handle(self, object_creator, x, y):
        if self.next:
            return self.next.handle(object_creator, x, y)

        return result_ok()


class IsCreatorHandler(AbstractHandler):
    def handle(self, object_creator, x, y):
        if not isinstance(object_creator, MapObjectCreator):
            return result_error('batch is not a map object creator')
        return super().handle(object_creator, x, y)


class OccupiedHandler(AbstractHandler):
    def handle(self, object_creator, x, y):
        if self.map_obj.get_cell(x, y).is_occupied():
            return result_error('cell is occupied')
        return super().handle(object_creator, x, y)


class LowAmountHandler(AbstractHandler):
    def handle(self, object_creator, x, y):
        if object_creator.amount == 0:
            return result_error('not enough creators')
        return super().handle(object_creator, x, y)


class CreatingHandler(AbstractHandler):
    def handle(self, object_creator, x, y):
        if not object_creator.matches_with_cell(self.map_obj.get_cell(x, y)):
            return result_error('cannot put there')
        return super().handle(object_creator, x, y)


class SafeCreator:
    def __init__(self, map_obj):
        self.map_obj = map_obj
        self.handler = IsCreatorHandler(map_obj)
        h2 = LowAmountHandler(map_obj)
        h3 = OccupiedHandler(map_obj)
        h4 = CreatingHandler(map_obj)
        self.handler.set_next(h2).set_next(h3).set_next(h4)

    def create_object(self, object_creator, x, y):
        res = self.handler.handle(object_creator, x, y)
        if res['ok']:
            object_creator.create_object(x, y)
        return res

    def remove_object(self, x, y):
        cell = self.map_obj.get_cell(x, y)
        cell.usable_object.remove()


if __name__ == '__main__':
    from core.virtual_objects.map_object_creators.concrete_creators import *
    from core.virtual_objects.materials.intermediates import IronPlate
    from maps import EasyMap
    import json

    map_object = EasyMap()

    NETWORKS = []

    with open('../map.json', 'r+') as f:
        map_object.load(json.load(f))

    burn_drill_creator = BurnerMiningDrillCreator(1, map_object)
    poll_creator = SmallElectricPoleCreator(2, map_object)
    generator_creator = BurnerElectricGeneratorCreator(2, map_object)
    i = IronPlate(1)

    object_creator1 = SafeCreator(map_object)
    print(object_creator1.create_object(i, 0, 0))
    print(generator_creator)
    # object_creator1.remove_object(0, 0)
    # print(object_creator1.create_object(generator_creator, 0, 0))
