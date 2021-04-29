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

    def add_pole(self, pole):
        self.poles.append(pole)


class ElectricPole(MapObject):
    wire_len: int
    coverage: int

    def __init__(self, x, y):
        super().__init__(x, y)
        self.network: ElectricNetwork = None

    def connect_to_network(self, network: ElectricNetwork):
        self.network = ElectricNetwork
        network.poles.append(self)


"""
Электрическая сеть, создающаяся при
создании пола

Сети дорожек, создающиеся с независимой дорожкой и
знающие начало, конец и длину
"""


class BurnerElectricGenerator:
    input_slots_num = 1
    valid_input = (Coal, Wood)
    max_power_output = 900

    def __init__(self):
        self.fuel = Container(self.input_slots_num)

    def put_energy(self, batch):
        if batch.is_fuel():
            self.fuel.put(batch)

    @property
    def power(self):
        return
