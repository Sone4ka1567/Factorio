from abc import ABC, abstractmethod
from base_classes import MapObject


class UsableObjectInterface(ABC):
    @abstractmethod
    def run(self):
        pass


class UsableObject(ABC, UsableObjectInterface, MapObject):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class UsableObjectProxy(UsableObjectInterface):
    def __init__(self, real_object: UsableObject):
        self._real_object = real_object
        self.progress = 0

    def _tick_react(self):
        self.progress += 1

    def run(self):
        self._tick_react()
        self._real_object.run()
