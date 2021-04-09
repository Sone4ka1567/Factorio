from pygamegui import PygameGUI
import constants as const


class Camera:
    def __init__(self, width, height):
        self.gui = PygameGUI()
        self.camera = self.gui.get_rect(0, 0, width, height)
        self.width, self.height = width, height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, player):
        x_border = -player.rect.x + int(const.DISPLAY_W / 2)
        y_border = -player.rect.y + int(const.DISPLAY_H / 2)

        x_border = min(0, x_border)  # left
        y_border = min(0, y_border)  # top
        x_border = max(-(self.width - const.DISPLAY_W), x_border)  # right
        y_border = max(-(self.height - const.DISPLAY_H), y_border)  # bottom

        self.camera = self.gui.get_rect(x_border, y_border, self.width, self.height)
