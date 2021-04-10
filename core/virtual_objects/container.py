from copy import deepcopy


class Container:
    def __init__(self, data=None):
        self.data = [] if data is None else data

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

    def produce_inside(self, target_batch):
        bag_copy = self.copy()
        requirements = target_batch.count_optimal_requirements(bag_copy)
        if not requirements:
            print('impossible')
            return False
        for requirement in requirements:
            print(requirement)
            self.remove(requirement)
        self.add(target_batch)
        print('res: ', self)
        return True

    def produce_outside(self, target_batch):
        requirements = target_batch.count_optimal_requirements(self)
        if not requirements:
            print('impossible')
            return False
        for requirement in requirements:
            self.remove(requirement)
        print('res: ', self)
        return True

    def __str__(self):
        if self.data:
            return str([str(batch) for batch in self.data])
        else:
            return "EMPTY BAG"
