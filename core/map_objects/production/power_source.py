from abc import abstractmethod, ABC
from core.container import Container


class PowerSource(ABC):
    def __init__(self, energy_consumption):
        self.energy_consumption = energy_consumption

    @abstractmethod
    def has_energy(self):
        pass

    @abstractmethod
    def subtract_energy(self):
        pass

    @abstractmethod
    def put_energy(self, *args):
        pass

    @abstractmethod
    def amount(self):
        pass

    @abstractmethod
    def finish_using(self):
        pass


class BurnerPowerSource(PowerSource):
    def __init__(self, energy_consumption):
        super().__init__(energy_consumption)
        self.fuel = Container(1)

    def has_energy(self):
        return (not self.fuel.is_empty()) and self.fuel[0].amount >= self.energy_consumption

    def subtract_energy(self):
        if self.fuel:
            self.fuel.remove(self.fuel[0].get_n(self.energy_consumption))

    def put_energy(self, fuel):
        if fuel.is_fuel():
            return self.fuel.put(fuel)
        return False

    def amount(self):
        return self.fuel

    def finish_using(self):
        pass


class Power:
    def __init__(self):
        self.power = 0


class ElectricPowerSource(PowerSource):
    def __init__(self, energy_consumption):
        super().__init__(energy_consumption)
        self.power = None
        self.is_used = False

    def has_energy(self):
        return self.power.power >= self.energy_consumption

    def subtract_energy(self):
        if not self.is_used:
            self.is_used = True
            self.power.power -= self.energy_consumption

    def put_energy(self, power: Power):
        self.power = power

    def amount(self):
        return self.power.power

    def finish_using(self):
        if self.is_used:
            self.is_used = False
            self.power.power += self.energy_consumption