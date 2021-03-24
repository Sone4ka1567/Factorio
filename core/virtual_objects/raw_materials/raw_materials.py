from base_classes import VirtualObject


class RawMaterial(VirtualObject):
    amount: int


class Iron(RawMaterial):
    def __init__(self, amount):
        self.amount = amount

    def convert_to_plates(self):
        pass
