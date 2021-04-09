from pygameGUI import PygameGUI
from constants import *
# паттерн стратегия


class Camera:
    def __init__(self, width, height):
        self.gui = PygameGUI()
        self.camera = self.gui.get_rect(0, 0, width, height)
        self.width, self.height = width, height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, player):
        x = -player.rect.x + int(DISPLAY_W / 2)
        y = -player.rect.y + int(DISPLAY_H / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - DISPLAY_W), x)  # right
        y = max(-(self.height - DISPLAY_H), y)  # bottom

        self.camera = self.gui.get_rect(x, y, self.width, self.height)






