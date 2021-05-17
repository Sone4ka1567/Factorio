from maps import Map, MapCell
from core.virtual_objects.materials.intermediates import Intermediate
from os.path import abspath


class MapObjectCreator(Intermediate):
    relative_image_path: str

    def __init__(self, object_type, amount, map_obj: Map):
        super().__init__(amount)
        self.object_type = object_type
        self.map_obj = map_obj

    def _put_map_object(self, x, y, created_object):
        cell = self.map_obj.get_cell(x, y)
        cell.usable_object = created_object
        self.amount -= 1

    def create_object(self, x, y):
        self._put_map_object(x, y, self.object_type(x, y, self.map_obj))

    def get_image_path(self):
        return abspath(self.relative_image_path.replace('../', ''))

    def matches_with_cell(self, cell: MapCell):
        return True

    def get_displayable_name(self):
        return self.object_type.__name__
