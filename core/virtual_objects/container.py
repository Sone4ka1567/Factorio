from copy import deepcopy


class Container:
    def __init__(self, data=None):
        self.data = [] if data is None else data

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
        res = target_batch.get_producing_result(
            self,
        )
        if not res:
            return False
        self.data = res[0].data
        self.add(target_batch)
        return res[1]

    def produce_outside(self, target_batch):
        res = target_batch.get_producing_result(
            self,
        )
        if not res:
            return False
        self.data = res[0].data
        return res[1]

    def __str__(self):
        if self.data:
            return str([str(batch) for batch in self.data])
        return "EMPTY BAG"
