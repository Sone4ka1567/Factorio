import json
from pygamegui import PygameSprite
import constants as const
from core.container import Container
from maps import MapCell
from result_func import result_ok, result_error

with open("player_perks.json", "r+") as f:
    player_perks = json.load(f)


class Player(PygameSprite):
    def __init__(self, game, x_spawn, y_spawn, bag_capacity, speed, picture):
        super().__init__()
        self.game = game
        self.groups = self.game.all_sprites
        self.init_sprite_and_group(self.groups)

        self.bag_capacity = bag_capacity
        self.bag = Container(bag_capacity)
        self.speed = speed
        self.image = self.gui.get_image(picture)
        self.image.set_colorkey(const.BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = x_spawn * const.CELL_SIZE
        self.rect.y = y_spawn * const.CELL_SIZE
        self.x = x_spawn * const.CELL_SIZE
        self.y = y_spawn * const.CELL_SIZE

    def update(self):
        self.speed_x = 0
        self.speed_y = 0
        direction = self.gui.get_keystate()
        if "LEFT" in direction:
            self.speed_x = -self.speed
        if "RIGHT" in direction:
            self.speed_x = self.speed
        if "UP" in direction:
            self.speed_y = -self.speed
        if "DOWN" in direction:
            self.speed_y = self.speed

        self.x += self.speed_x
        self.y += self.speed_y
        self.rect.x = self.x
        self.rect.y = self.y

        if self.rect.right > const.PIXEL_MAP_W:
            self.rect.right = const.PIXEL_MAP_W
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > const.PIXEL_MAP_H:
            self.rect.bottom = const.PIXEL_MAP_H
        if self.rect.top < 0:
            self.rect.top = 0

    def collide_with_trees(self):
        pass

    def dig(self, cell: MapCell):
        if cell.raw_material_batch:
            res = self.bag.put(cell.raw_material_batch.get_n(1))
            if not res:
                return result_error("cannot dig: bag is full")
            cell.raw_material_batch.amount -= 1
            if cell.raw_material_batch.amount == 0:
                cell.raw_material_batch = None
            return result_ok(f"+1 {cell.raw_material_batch.__class__.__name__}")
        return result_error("nothing to dig here")
