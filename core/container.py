from copy import deepcopy


class Container:
    def __init__(self, max_size, data=None):
        self.max_size = max_size
        self.data = [] if data is None else data

    def is_empty(self):
        return len(self.data) == 0

    def contains(self, batch):
        for cur_batch in self.data:
            # print(type(batch), '-', type(cur_batch))
            if isinstance(cur_batch, type(batch)):
                return cur_batch.amount >= batch.amount
        return False

    def contains_type(self, batch):
        for cur_batch in self.data:
            if isinstance(cur_batch, type(batch)):
                return True
        return False

    def put(self, batch):
        done = False
        for idx, cur_batch in enumerate(self.data):
            if isinstance(cur_batch, type(batch)):
                self.data[idx].amount += batch.amount
                done = True
        if not done and len(self.data) < self.max_size:
            self.data.append(batch)
        return True

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
        if len(self.data) == self.max_size:
            return False
        res = target_batch.get_producing_result(self)
        if not res:
            return False
        self.data = res[0].data
        self.put(target_batch)
        return res[1]

    def produce_outside(self, target_batch):
        res = target_batch.get_producing_result(self)
        if not res:
            return False
        self.data = res[0].data
        return res[1]

    def __getitem__(self, item):
        return self.data[item]

    def __str__(self):
        if self.data:
            return str([str(batch) for batch in self.data])
        return "EMPTY BAG"
