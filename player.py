from constants import *
from pygameGUI import PygameSprite


player_perks = {
    'balanced': {
        'speed': 9,
        'bag_capacity': 35,
        'picture': 'player_walk1.png'
    },
    'fast': {
        'speed': 12,
        'bag_capacity': 30,
        'picture': 'female_walk1.png'
    },
    'big_bag': {
        'speed': 6,
        'bag_capacity': 40,
        'picture': 'adventurer_walk1.png'
    }
}


class Player(PygameSprite):
    def __init__(self, bag_capacity, speed, picture):
        super().__init__()
        self.bag = {}
        self.bag_capacity = bag_capacity
        self.speed = speed
        self.image = self.gui.get_image(picture)

        self.rect = self.image.get_rect()
        self.rect.centerx = DISPLAY_W / 2
        self.rect.bottom = DISPLAY_H / 2

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
        if self.rect.right > DISPLAY_W:
            self.rect.right = DISPLAY_W
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > DISPLAY_H:
            self.rect.bottom = DISPLAY_H
        if self.rect.top < 0:
            self.rect.top = 0

    def dig(self, *args):
        # todo: реализовать копание
        pass
