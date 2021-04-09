from constants import *
import json
from pygameGUI import PygameSprite, PygameGUI

with open('player_perks.json', 'r+') as f:
    player_perks = json.load(f)


class Player(PygameSprite):
    def __init__(self, game, x_spawn, y_spawn, bag_capacity, speed, picture):
        super().__init__()
        self.gui = PygameGUI()
        self.game = game
        self.groups = self.game.all_sprites
        self.init_sprite_and_group(self.groups)

        self.bag = {}
        self.bag_capacity = bag_capacity
        self.speed = speed
        self.image = self.gui.get_image(picture)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = x_spawn * CELL_SIZE
        self.rect.y = y_spawn * CELL_SIZE

    def update(self):
        self.speedx = 0
        self.speedy = 0
        direction = self.gui.get_keystate()
        if direction == 'LEFT':
            self.speedx = -self.speed
        if direction == 'RIGHT':
            self.speedx = self.speed
        if direction == 'UP':
            self.speedy = -self.speed
        if direction == 'DOWN':
            self.speedy = self.speed

        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > PIXEL_MAP_W:
            self.rect.right = PIXEL_MAP_W
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > PIXEL_MAP_H:
            self.rect.bottom = PIXEL_MAP_H
        if self.rect.top < 0:
            self.rect.top = 0

    def dig(self, *args):
        # todo: реализовать копание
        pass
