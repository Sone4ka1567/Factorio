from pygamegui import PygameSprite
import constants as const


class UsableObjectSprite(PygameSprite):

    def __init__(self, game, x_spawn, y_spawn, map_obj, img):
        super().__init__()
        self.game = game
        self.groups = game.all_sprites, game.usable_objects
        self.init_sprite_and_group(self.groups)
        self.map_obj = map_obj
        self.category = 'usable'

        self.image = self.gui.get_image(img)
        self.image.set_colorkey(const.BLACK)
        self.rect = self.image.get_rect()

        self.x_spawn = x_spawn
        self.y_spawn = y_spawn
        self.rect.x = self.x_spawn * const.CELL_SIZE
        self.rect.y = self.y_spawn * const.CELL_SIZE