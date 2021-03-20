import pygame
from constants import *
# паттерн стратегия

vec = pygame.math.Vector2


class Camera:
    def __init__(self):
        self.camera = pygame.Rect(0, 0, DISPLAY_W, DISPLAY_H)
        self.width, self.height = DISPLAY_W, DISPLAY_H

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, player):
        x = -player.rect.x + int(DISPLAY_W / 2)
        y = - player.rect.y + int(DISPLAY_H / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - DISPLAY_W), x)  # right
        y = max(-(self.height - DISPLAY_H), y)  # bottom

        self.camera = pygame.Rect(x, y, self.width, self.height)






