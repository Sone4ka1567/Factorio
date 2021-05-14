from map_object import MapObject
from core.container import Container
from basic_geometry import euclidean_dist
from result_func import result_ok, result_error


class Power:
    def __init__(self):
        self.value = 0


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
            print("not found pole")
            nearest_generator = find_nearest(
                self.x, self.y, self.wire_len, self.map_obj, BurnerElectricGenerator
            )
            if nearest_generator:
                print("found gen")
                self.connect_to_generator(nearest_generator)
            else:
                print("not found gen")

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
                if obj.needs_energy() and obj.needs_electric_energy() and not obj.has_energy():
                    obj.put_energy(self.power)

    def disconnect_machines(self):
        for dx in range(-self.coverage_rad, self.coverage_rad):
            for dy in range(-self.coverage_rad, self.coverage_rad):
                if dx == 0 and dy == 0:
                    continue
                obj = self.map_obj.get_cell(self.x + dx, self.y + dy).usable_object
                if obj.needs_energy() and obj.needs_electric_energy():
                    obj.remove_energy()

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
        return f"p: {id(self.power)}, p: {self.priority}"


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
        self.power_scheme = {1: 0.2,
                             2: 0.5,
                             3: 0.8}

        nearest_pole = find_nearest(
            self.x, self.y, self.coverage_rad, self.map_obj, ElectricPole
        )
        if nearest_pole and nearest_pole.priority == -1:
            self.connect_to_pole(nearest_pole)

    def power_func(self):
        if self.fuel.is_empty():
            return 0
        if self.fuel[0].amount > max(self.power_scheme.keys()):
            return self.max_power_output
        return int(self.power_scheme[self.fuel[0].amount] * self.max_power_output)

    def connect_to_pole(self, pole: ElectricPole):
        pole.connect_to_generator(self)
        self.is_connected_to_pole = True

    def disconnect_pole(self):
        self.is_connected_to_pole = False

    def put_energy(self, batch):
        if batch.is_fuel():
            self.fuel.put(batch)
            return result_ok()
        return result_error('not a fuel')

    def process(self):
        self.power.value = self.power_func()

    def get_power(self):
        return self.power

    def is_connected(self):
        return self.is_connected_to_pole

    def __str__(self):
        return f"G: {id(self.power)}"


class SmallElectricPole(ElectricPole):
    wire_len: int = 5
    coverage_rad: int = 3


class BigElectricPole(ElectricPole):
    wire_len: int = 8
    coverage_rad: int = 5
