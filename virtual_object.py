from abc import ABC


class VirtualObject(ABC):
    def __init__(self, amount):
        self.amount = amount
