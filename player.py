from base_classes import MapObject

player_perks = {
    'balanced': {
        'speed': 9,
        'bag_capacity': 35
    },
    'fast': {
        'speed': 12,
        'bag_capacity': 30,
    },
    'big_bag': {
        'speed': 6,
        'bag_capacity': 40
    }
}


class Player(MapObject):
    def __init__(self, bag_capacity, speed):
        self.bag = {}
        self.bag_capacity = bag_capacity
        self.speed = speed

    def dig(self, *args):
        # todo: реализовать копание
        pass

    def update(self):
        # todo: реализовать обновление
        pass
