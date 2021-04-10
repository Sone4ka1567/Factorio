class Container:
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
                if cur_batch.amount > batch.amount:
                    self.data[idx].amount -= batch.amount
                else:
                    self.data[idx] = None

    def get_data(self):
        return self.data
