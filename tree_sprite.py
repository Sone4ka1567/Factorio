from pygamegui import PygameSprite
import constants as const


class Tree(PygameSprite):
    def __init__(self, game, x_spawn, y_spawn):
        super().__init__()
        self.game = game
        self.groups = game.all_sprites, game.trees
        self.init_sprite_and_group(self.groups)

        self.image = self.gui.get_image("trees/tree01.xcf")
        self.image.set_colorkey(const.BLACK)
        # self.image = pygame.Surface((const.CELL_SIZE, const.CELL_SIZE))
        # self.image.fill(const.BLACK)
        self.rect = self.image.get_rect()

        self.cut_tree_image = self.gui.get_image("trees/cut_tree01.png")

        self.rect.centerx = x_spawn * const.CELL_SIZE + const.CELL_SIZE // 2
        self.rect.bottom = (y_spawn + 1) * const.CELL_SIZE - const.CELL_SIZE // 3
        # self.rect.x = x_spawn * const.CELL_SIZE
        # self.rect.y = y_spawn * const.CELL_SIZE
