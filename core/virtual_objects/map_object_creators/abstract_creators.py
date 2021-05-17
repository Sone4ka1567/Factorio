from maps import Map, MapCell
from core.virtual_objects.materials.intermediates import Intermediate


class MapObjectCreator(Intermediate):
    def __init__(self, object_type, amount, map_obj: Map):
        super().__init__(amount)
        self.object_type = object_type
        self.map_obj = map_obj

    def _put_map_object(self, x, y, created_object, real_map: Map):
        cell = real_map.get_cell(x, y)
        cell.usable_object = created_object
        # real_map.set_cell(x, y, cell)
        self.amount -= 1

    def create_object(self, x, y):
        self._put_map_object(x, y, self.object_type(x, y, self.map_obj), self.map_obj)

    def matches_with_cell(self, cell: MapCell):
        return True

    def get_displayable_name(self):
        return self.object_type.__name__
