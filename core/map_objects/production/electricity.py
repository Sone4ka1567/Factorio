from map_object import MapObject
from core.container import Container
from maps import Map


class Power:
    def __init__(self, map_object, generator_coordinates=None):
        self.generator_coordinates = generator_coordinates
        self.map_obj: Map = map_object

    def set_generator(self, generator_coordinates):
        self.generator_coordinates = generator_coordinates

    @property
    def power(self):
        return (
            self.map_obj.get_usable_object(*self.generator_coordinates).get_power()
            if self.generator_coordinates
            else 0
        )


class ElectricNetwork:
    def __init__(self, map_obj):
        self.power = Power(map_obj)
        self.poles = []
        self.has_generator = False

    def add_pole(self, pole):
        self.poles.append(pole)

    def add_generator(self, generator):
        self.has_generator = True
        self.power.set_generator((generator.x, generator.y))

    def get_power(self):
        return self.power

    def __str__(self):
        return (
            f"poles: {[str(i) for i in self.poles]}, has_generator: {self.has_generator},"
            f" power: {None if not self.power else self.power.power}"
        )


class ElectricPole(MapObject):
    wire_len: int = 2
    coverage_rad: int = 4

    def __init__(self, x, y, map_obj):
        super().__init__(x, y, map_obj)
        self.network: ElectricNetwork = None

    def connect_to_network(self, network: ElectricNetwork):
        self.network = network
        network.add_pole(self)

    def process(self):
        pass

    def __str__(self):
        return f"pole: ({self.x}, {self.y})"


class SmallElectricPole(ElectricPole):
    wire_len: int = 2
    coverage_rad: int = 2


class BigElectricPole(ElectricPole):
    wire_len: int = 4
    coverage_rad: int = 8


"""
Электрическая сеть, создающаяся при
создании столба

Сети дорожек, создающиеся с независимой дорожкой и
знающие начало, конец и длину
"""


class BurnerElectricGenerator(MapObject):
    input_slots_num = 1
    max_power_output = 900
    wire_len = 2

    def __init__(self, x, y, map_obj):
        super().__init__(x, y, map_obj)
        self.fuel = Container(self.input_slots_num)
        self.power = 0
        self.network: ElectricNetwork = None

    def put_energy(self, batch):
        if batch.is_fuel():
            self.fuel.put(batch)

    def process(self):
        self.power = 0 if self.fuel.is_empty() else self.max_power_output

    def get_power(self):
        return self.power

    def connect_to_network(self, network: ElectricNetwork):
        self.network = ElectricNetwork
        network.add_generator(self)
