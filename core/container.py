from copy import deepcopy
from result_func import result_ok, result_error


class Container:
    def __init__(self, max_size, data=None):
        self.max_size = max_size
        self.data = [] if data is None else list(data)

    def is_empty(self):
        return len(self.data) == 0

    def contains(self, batch):
        for cur_batch in self.data:
            if isinstance(cur_batch, type(batch)):
                return cur_batch.amount >= batch.amount
        return False

    def contains_type(self, batch):
        for cur_batch in self.data:
            if isinstance(cur_batch, type(batch)):
                return True
        return False

    def put(self, batch):
        for idx, cur_batch in enumerate(self.data):
            if isinstance(cur_batch, type(batch)):
                self.data[idx].amount += batch.amount
                return True
        if len(self.data) < self.max_size:
            self.data.append(batch)
            return True
        return False

    def remove(self, batch):
        for idx, cur_batch in enumerate(self.data):
            if isinstance(cur_batch, type(batch)):
                if cur_batch.amount > batch.amount:
                    self.data[idx].amount -= batch.amount
                    return
                self.data.pop(idx)
                return

    def get_data(self):
        return self.data

    def copy(self):
        return Container(deepcopy(self.data))

    def produce_inside(self, target_batch):
        if len(self.data) == self.max_size:
            return result_error('bag is full')
        res = target_batch.get_producing_result(self)
        if not res:
            return result_error('not enough resources')
        self.data = res[0].data
        self.put(target_batch)
        return result_ok(content=res[1])

    def produce_outside(self, target_batch):
        res = target_batch.get_producing_result(self)
        if not res:
            return result_error('not enough resources')
        self.data = res[0].data
        return result_ok(content=res[1])

    def __getitem__(self, item):
        return self.data[item]

    def __str__(self):
        if self.data:
            return str([str(batch) for batch in self.data])
        return "EMPTY BAG"


if __name__ == '__main__':
    from core.virtual_objects.map_object_creators.concrete_creators import BurnerAssemblingMachineCreator
    from maps import EasyMap

    map = EasyMap()
    player_bag = Container(10)
    # player_bag.put()
    r = player_bag.produce_inside(BurnerAssemblingMachineCreator(2, map))
    print(r)
