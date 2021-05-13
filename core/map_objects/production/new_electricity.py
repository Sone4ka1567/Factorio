from map_object import MapObject
from core.container import Container
from math import sqrt
from core.map_objects.production.machine import Machine
from core.map_objects.production.power_source import ElectricPowerSource


class Power:
    def __init__(self):
        self.value = 0


def euclidean_dist(dx, dy):
    return sqrt(dx ** 2 + dy ** 2)


def find_nearest(x, y, max_distance, map_obj, object_type, condition=lambda x: True):
    # print(object_type)
    nearest_objects = {}
    for dx in range(-max_distance, max_distance):
        for dy in range(-max_distance, max_distance):
            if dx == 0 and dy == 0:
                continue
            obj = map_obj.get_cell(x + dx, y + dy).usable_object
            # print(obj)
            if isinstance(obj, object_type) and condition(obj):
                nearest_objects = {euclidean_dist(dx, dy): obj}
    # if object_type == ElectricPole:
    #     exit()
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
    #         x, y, ElectricPole.wire_len, map_obj, ElectricGenerator
    #     )
    #     if nearest_generator:
    #         return result_ok()
    #     return result_error('cannot create: no generator or pole around')

    def __init__(self, x, y, map_obj):
        super().__init__(x, y, map_obj)
        self.connected_poles = []
        self.power = None
        self.priority = -1  # in line with no generator
        self.generator = None

        nearest_pole = find_nearest(
            self.x, self.y, self.wire_len, self.map_obj, ElectricPole
        )
        if nearest_pole:
            self.connect_to_pole(nearest_pole)
        else:
            print('not found pole')
            nearest_generator = find_nearest(
                self.x, self.y, self.wire_len, self.map_obj, BurnerElectricGenerator
            )
            if nearest_generator:
                print('found gen')
                self.connect_to_generator(nearest_generator)
            else:
                print('not found gen')

        # todo: подключить все машины
        self.connect_machines()

    def connect_to_pole(self, pole):
        self.connected_poles.append(pole)
        pole.connected_poles.append(self)
        self.power = pole.power
        self.priority = -1 if pole.priority == -1 else pole.priority + 1

    def connect_to_generator(self, generator):
        def dfs(cur_pole: ElectricPole, priority, power):
            cur_pole.priority = priority
            cur_pole.power = power
            for connected_pole in cur_pole.connected_poles:
                dfs(connected_pole, priority + 1, power)

        dfs(self, 0, generator.power)
        self.generator = generator

    def connect_machines(self):
        for dx in range(-self.coverage_rad, self.coverage_rad):
            for dy in range(-self.coverage_rad, self.coverage_rad):
                if dx == 0 and dy == 0:
                    continue
                obj = self.map_obj.get_cell(self.x + dx, self.y + dy).usable_object
                print(self.x + dx, self.y + dy)
                if (
                        isinstance(obj, Machine)
                        and isinstance(obj.energy_source, ElectricPowerSource)
                        and obj.energy_source.power is None
                ):
                    obj.energy_source.put_energy(self.power)

    def disconnect_machines(self):
        for dx in range(-self.coverage_rad, self.coverage_rad):
            for dy in range(-self.coverage_rad, self.coverage_rad):
                if dx == 0 and dy == 0:
                    continue
                obj = self.map_obj.get_cell(self.x + dx, self.y + dy).usable_object
                if (
                        isinstance(obj, Machine)
                        and isinstance(obj.energy_source, ElectricPowerSource)
                ):
                    obj.energy_source.remove_energy()

        for connected_pole in self.connected_poles:
            connected_pole.connect_machines()

    def _disconnect_all(self):
        for pole in self.connected_poles:
            for idx, con_pol in enumerate(pole.connected_poles):
                if con_pol == self:
                    pole.connected_poles.pop(idx)

        def dfs(cur_pole: ElectricPole, priority):
            cur_pole.power = None
            cur_pole.priority = -1
            for connected_pole in cur_pole.connected_poles:
                if connected_pole.priority > priority:
                    dfs(connected_pole, priority)

        dfs(self, self.priority)

        if self.priority == 0:
            self.generator.disconnect_pole()

        self.disconnect_machines()

    def remove(self):
        self._disconnect_all()
        self._clear_cell()

    def is_connected(self):
        return self.power is not None

    def process(self):
        pass

    def __str__(self):
        return f'p: {id(self.power)}, p: {self.priority}'


class ElectricGenerator(MapObject):
    def process(self):
        pass


class BurnerElectricGenerator(ElectricGenerator):
    input_slots_num = 1
    max_power_output = 900
    coverage_rad = 10

    def __init__(self, x, y, map_obj):
        super().__init__(x, y, map_obj)
        self.fuel = Container(self.input_slots_num)
        self.power = Power()
        self.is_connected_to_pole = False

        nearest_pole = find_nearest(
            self.x, self.y, self.coverage_rad, self.map_obj, ElectricPole
        )
        if nearest_pole and nearest_pole.priority == -1:
            self.connect_to_pole(nearest_pole)

    def connect_to_pole(self, pole: ElectricPole):
        pole.connect_to_generator(self)
        self.is_connected_to_pole = True

    def disconnect_pole(self):
        self.is_connected_to_pole = False

    def put_energy(self, batch):
        if batch.is_fuel():
            self.fuel.put(batch)

    def process(self):
        self.power.value = 0 if self.fuel.is_empty() else self.max_power_output

    def get_power(self):
        return self.power

    def is_connected(self):
        return self.is_connected_to_pole

    def __str__(self):
        return f'G: {id(self.power)}'


class SmallElectricPole(ElectricPole):
    wire_len: int = 5
    coverage_rad: int = 3


class BigElectricPole(ElectricPole):
    wire_len: int = 8
    coverage_rad: int = 5


if __name__ == '__main__':
    from maps import EasyMap, MapCell
    import json

    map = EasyMap()
    with open(r'C:\Users\79161\PycharmProjects\patterns-project\map.json', 'r+') as f:
        map.load(json.load(f))
    Y = 100
    X = 60

    cell: MapCell = map.get_cell(X, Y)
    cell.usable_object = BurnerElectricGenerator(X, Y, map)
    for x in range(X + 5, 85, 5):
        # x = X + 1
        cell: MapCell = map.get_cell(x, Y)
        cell.usable_object = SmallElectricPole(x, Y, map)

    Y2 = Y + 1
    cell: MapCell = map.get_cell(X + 10, Y2)
    cell.usable_object = SmallElectricPole(X + 10, Y2, map)

    cell: MapCell = map.get_cell(X + 10, Y)
    # cell.usable_object.remove()

    from core.map_objects.production.production import ElectricAssemblingMachine

    cell: MapCell = map.get_cell(X + 5, Y + 1)
    cell.usable_object = ElectricAssemblingMachine(X + 5, Y + 1, map)
    #
    cell1: MapCell = map.get_cell(X, Y + 2)
    cell1.usable_object = BurnerElectricGenerator(X, Y + 2, map)
    print('SUUUUKAAAAA')
    cell2: MapCell = map.get_cell(X + 5, Y + 2)
    cell2.usable_object = SmallElectricPole(X + 5, Y + 2, map)


    #
    # print(f"|{map.get_cell(X, Y).usable_object}|\t", end='')
    #
    # print(f"|{map.get_cell(x, Y).usable_object}|\t", end='')
    def log():
        for yy in range(Y, Y + 3):
            for xx in range(X, 85, 1):
                s = f"|{map.get_cell(xx, yy).usable_object}|"
                print(s + ' ' * max(28 - len(s), 0), end='')
            print()


    log()

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
