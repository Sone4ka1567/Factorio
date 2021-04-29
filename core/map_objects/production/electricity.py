from core.map_objects.production.machine import Machine
from core.virtual_objects.materials.raw_and_basics import Coal, Wood
from base_classes import MapObject
from core.container import Container


class Power:
    def __init__(self):
        self.power = 0


class ElectricNetwork:
    def __init__(self):
        self.power = Power()
        self.poles = []
        self.has_generator = False

    def add_pole(self, pole):
        self.poles.append(pole)

    def add_generator(self, generator):
        self.has_generator = True
        self.power = generator.get_power()


class ElectricPole(MapObject):
    wire_len: int
    coverage_rad: int

    def __init__(self, x, y):
        super().__init__(x, y)
        self.network: ElectricNetwork = None

    def connect_to_network(self, network: ElectricNetwork):
        self.network = ElectricNetwork
        network.add_pole(self)


"""
Электрическая сеть, создающаяся при
создании пола

Сети дорожек, создающиеся с независимой дорожкой и
знающие начало, конец и длину
"""


class BurnerElectricGenerator(MapObject):
    input_slots_num = 1
    max_power_output = 900
    wire_len = 2

    def __init__(self, x, y):
        super().__init__(x, y)
        self.fuel = Container(self.input_slots_num)
        self.power = Power()
        self.network: ElectricNetwork = None

    def put_energy(self, batch):
        if batch.is_fuel():
            self.fuel.put(batch)

    def process(self):
        self.power.power = 0 if self.fuel.is_empty() else self.max_power_output

    def get_power(self):
        return self.power

    def connect_to_network(self, network: ElectricNetwork):
        self.network = ElectricNetwork
        network.add_generator(self)
