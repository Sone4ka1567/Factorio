import os
import sys

import pygame
from facade import GUI


class PygameSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.speed_x = 0
        self.speed_y = 0
        self.gui = PygameGUI()

    def init_sprite_and_group(self, group):
        pygame.sprite.Sprite.__init__(self, group)

    def sprite_collision(self, group, do_kill):
        return pygame.sprite.spritecollide(self, group, do_kill)


class PygameGUI(GUI):

    def start(self):
        # pylint: disable=no-member
        pygame.init()
        # pylint: enable=no-member

    def set_caption(self, caption):
        pygame.display.set_caption(caption)

    def set_screen(self, width, height, hwsurf, double_buffer):
        return pygame.display.set_mode((width, height), hwsurf | double_buffer)

    def fill_screen(self, screen, color):
        screen.fill(color)

    def set_clock(self):
        return pygame.time.Clock()

    def tick_fps(self, clock, fps):
        return clock.tick(fps)

    def group_sprites(self):
        return pygame.sprite.Group()

    def update_sprites(self, group):
        group.update()

    def draw_group(self, group, screen):
        group.draw(screen)

    def add_sprite(self, group, sprite):
        group.put(sprite)

    def get_surface(self, width, height):
        return pygame.Surface((width, height))

    def get_image(self, image):
        game_folder = os.path.dirname(__file__)
        img_folder = os.path.join(game_folder, "img")
        return pygame.image.load(os.path.join(img_folder, image)).convert()

    def get_display_info(self):
        return pygame.display.Info().current_w, pygame.display.Info().current_h

    def get_rect(self, x_border, y_border, width, height):
        return pygame.Rect(x_border, y_border, width, height)

    def get_mouse_pos(self):
        return pygame.mouse.get_pos()

    def get_mouse_pressed(self):
        return pygame.mouse.get_pressed(3)

    def get_keystate(self):
        keystate = pygame.key.get_pressed()
        # pylint: disable=no-member
        lst = []
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            lst.append("LEFT")
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            lst.append("RIGHT")
        if keystate[pygame.K_UP] or keystate[pygame.K_w]:
            lst.append("UP")
        if keystate[pygame.K_DOWN] or keystate[pygame.K_s]:
            lst.append("DOWN")
        if keystate[pygame.K_e]:
            lst.append("E")
        if keystate[pygame.K_ESCAPE]:
            lst.append("ESCAPE")
        # pylint: enable=no-member
        return lst

    def get_events(self):
        return pygame.event.get()

    def get_event_type(self, event):
        # pylint: disable=no-member
        if event.type == pygame.QUIT:
            return "QUIT"

        if event.type == pygame.MOUSEBUTTONDOWN:
            return 'MOUSEBUTTONDOWN'

        # pylint: enable=no-member
        return None

    def draw_line(self, screen, color, start, end):
        pygame.draw.line(screen, color, start, end)

    def draw_rect(self, screen, color, coordinates):
        pygame.draw.rect(screen, color, coordinates)

    def get_font(self, name, size):
        return pygame.font.Font(name, size)

    def get_sys_font(self, name, size):
        return pygame.font.SysFont(name, size)

    def flip_display(self):
        pygame.display.flip()

    def update_display(self):
        pygame.display.update()

    def get_hwsurface(self):
        return pygame.HWSURFACE

    def get_double_buffer(self):
        return pygame.DOUBLEBUF

    def quit_game(self):
        # pylint: disable=no-member
        pygame.quit()
        sys.exit()
        # pylint: enable=no-member
