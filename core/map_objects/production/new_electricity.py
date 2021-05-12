from base_classes import MapObject
from core.container import Container
from maps import Map
from math import sqrt
from result_func import result_ok, result_error


class Power:
    def __init__(self):
        self.value = 0


def euclidean_dist(dx, dy):
    return sqrt(dx ** 2 + dy ** 2)


def find_nearest(x, y, max_distance, map_obj, object_type, condition=lambda x: True):
    nearest_objects = {}
    for dx in range(-max_distance, max_distance):
        for dy in range(-max_distance, max_distance):
            if dx == 0 and dy == 0:
                continue
            obj = map_obj.get_cell(x + dx, y + dy).usable_object
            if isinstance(obj, object_type) and condition(obj):
                nearest_objects = {euclidean_dist(dx, dy): obj}
    if nearest_objects:
        return nearest_objects[min(nearest_objects.keys())]
    return None


class ElectricPole(MapObject):
    wire_len: int = 2
    coverage_rad: int = 4

    # @staticmethod
    # def can_be_created(x, y, map_obj):
    #     nearest_pole = find_nearest(
    #         x, y, ElectricPole.wire_len, map_obj, ElectricPole
    #     )
    #     if nearest_pole:
    #         return result_ok()
    #
    #     nearest_generator = find_nearest(
    #         x, y, ElectricPole.wire_len, map_obj, BurnerElectricGenerator
    #     )
    #     if nearest_generator:
    #         return result_ok()
    #     return result_error('cannot create: no generator or pole around')

    def __init__(self, x, y, map_obj):
        super().__init__(x, y, map_obj)
        self.connected_poles = []
        self.power = None
        self.priority = -1  # not in a network

        nearest_pole = find_nearest(
            self.x, self.y, self.wire_len, self.map_obj, ElectricPole
        )
        if nearest_pole:
            self.connect_to_pole(nearest_pole)
            return

        nearest_generator = find_nearest(
            self.x, self.y, self.wire_len, self.map_obj, BurnerElectricGenerator
        )
        if nearest_generator:
            self.connect_to_generator(nearest_generator)

    def connect_to_pole(self, pole):
        self.connected_poles.append(pole)
        pole.connected_poles.append(self)
        self.power = pole.power
        self.priority = pole.priority + 1

    def connect_to_generator(self, generator):

        def dfs(cur_pole: ElectricPole, priority):
            cur_pole.priority = priority
            for connected_pole in cur_pole.connected_poles:
                dfs(connected_pole, priority + 1)

        self.power = generator.power
        dfs(self, 0)

    def _disconnect_all(self):
        for pole in self.connected_poles:
            for idx, con_pol in enumerate(pole.connected_poles):
                pole.connected_poles.pop(idx)
                if con_pol.priority > self.priority:
                    pole.power = None
                    con_pol.priority = -1

    def remove(self):
        self._disconnect_all()
        self._clear_cell()

    def is_connected(self):
        return not (self.power is None)

    def process(self):
        pass


class SmallElectricPole(ElectricPole):
    wire_len: int = 2
    coverage_rad: int = 2


class BigElectricPole(ElectricPole):
    wire_len: int = 4
    coverage_rad: int = 8


class BurnerElectricGenerator(MapObject):
    input_slots_num = 1
    max_power_output = 900
    coverage_rad = 10

    def __init__(self, x, y, map_obj):
        super().__init__(x, y, map_obj)
        self.fuel = Container(self.input_slots_num)
        self.power = Power()

        nearest_pole = find_nearest(
            self.x, self.y, self.coverage_rad, self.map_obj, ElectricPole
        )
        if nearest_pole:
            self.connect_to_pole(nearest_pole)

    def connect_to_pole(self, pole: ElectricPole):
        pole.connect_to_generator(self)

    def put_energy(self, batch):
        if batch.is_fuel():
            self.fuel.put(batch)

    def process(self):
        self.power.value = 0 if self.fuel.is_empty() else self.max_power_output

    def get_power(self):
        return self.power

# if __name__ == '__main__':
#     class H:
#         def __init__(self, link):
#             self.linked = link
#
#     class P:
#         def __init__(self):
#             self.value = 0
#
#     p = P()
#     p.value = 10
#     h = H(p)
#     h2  = H(0)
#     h2.linked = h.linked
#     del h
#     p.value -= 5
#     print(h2.linked.value)