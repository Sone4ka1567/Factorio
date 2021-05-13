from abc import abstractmethod, ABC
from core.container import Container
from core.map_objects.production.electricity import Power


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
    def remove_energy(self):
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
        return (
                not self.fuel.is_empty() and self.fuel[0].amount >= self.energy_consumption
        )

    def subtract_energy(self):
        if self.fuel:
            self.fuel.remove(self.fuel[0].get_n(self.energy_consumption))

    def put_energy(self, fuel):
        if fuel.is_fuel():
            return self.fuel.put(fuel)
        return False

    def remove_energy(self):
        f = self.fuel
        self.fuel = None
        return f

    def amount(self):
        return self.fuel

    def finish_using(self):
        pass


class ElectricPowerSource(PowerSource):
    def __init__(self, energy_consumption):
        super().__init__(energy_consumption)
        self.power = None

    def has_energy(self):
        return self.power.value >= self.energy_consumption

    def subtract_energy(self):
        self.power.value -= self.energy_consumption

    def put_energy(self, power: Power):
        self.power = power

    def remove_energy(self):
        self.power = None

    def amount(self):
        return self.power.value if self.power else 0

    def finish_using(self):
        self.power.value += self.energy_consumption
