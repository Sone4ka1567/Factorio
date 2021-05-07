from pygamegui import PygameSprite
import constants as const


class Tree(PygameSprite):
    def __init__(self, game, x_spawn, y_spawn, map_obj):
        super().__init__()
        self.game = game
        self.groups = game.all_sprites, game.trees
        self.init_sprite_and_group(self.groups)
        self.map_obj = map_obj
        self.category = 'tree'

        self.image = self.gui.get_image("trees/tree01.xcf")
        self.image.set_colorkey(const.BLACK)
        self.rect = self.image.get_rect()

        self.x_spawn = x_spawn
        self.y_spawn = y_spawn
        self.rect.centerx = self.x_spawn * const.CELL_SIZE + const.CELL_SIZE // 2
        self.rect.bottom = (self.y_spawn + 1) * const.CELL_SIZE - const.CELL_SIZE // 3

    def change_image(self):
        self.image = self.gui.get_image("trees/cut_tree01.png")
        self.image.set_colorkey(const.BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.x_spawn * const.CELL_SIZE + const.CELL_SIZE // 2
        self.rect.bottom = (self.y_spawn + 1) * const.CELL_SIZE - const.CELL_SIZE // 3
