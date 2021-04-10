from copy import deepcopy


class Container:
    def __init__(self, data=None):
        self.data = [] if data is None else data

    def contains(self, batch):
        for cur_batch in self.data:
            if isinstance(cur_batch, type(batch)):
                return cur_batch.amount >= batch.amount
        return False

    def add(self, batch):
        done = False
        for idx, cur_batch in enumerate(self.data):
            if isinstance(cur_batch, type(batch)):
                self.data[idx].amount += batch.amount
                done = True
        if not done:
            self.data.append(batch)

    def remove(self, batch):
        for idx, cur_batch in enumerate(self.data):
            if isinstance(cur_batch, type(batch)):
                if cur_batch.amount > batch.amount:
                    self.data[idx].amount -= batch.amount
                else:
                    self.data.pop(idx)

    def get_data(self):
        return self.data

    def copy(self):
        return Container(deepcopy(self.data))

    def can_produce(self, target_batch):
        bag_copy = self.copy()
        res = target_batch.count_requirements(bag_copy)
        if res:
            self.data = bag_copy.data
            print('without res: ', self)
            return True
        print('impossible')
        return False

    def produce_inside(self, target_batch):
        if self.can_produce(target_batch):
            self.add(target_batch)
            print('with res:', self)
            return True
        return False

    def __str__(self):
        if self.data:
            return str([str(batch) for batch in self.data])
        else:
            return "EMPTY BAG"
