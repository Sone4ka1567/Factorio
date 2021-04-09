import os
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
    def __init__(self):
        super().__init__()

    def start(self):
        # pylint: disable=no-member
        pygame.init()
        # pylint: enable=no-member

    def set_caption(self, caption):
        pygame.display.set_caption(caption)

    def set_screen(self, width, height):
        return pygame.display.set_mode((width, height))

    def fill_screen(self, screen, color):
        screen.fill(color)

    def set_clock(self):
        return pygame.time.Clock()

    def set_fps(self, clock, fps):
        clock.tick(fps)

    def group_sprites(self):
        return pygame.sprite.Group()

    def update_sprites(self, group):
        group.update()

    def draw_group(self, group, screen):
        group.draw(screen)

    def add_sprite(self, group, sprite):
        group.add(sprite)

    def get_surface(self, width, height):
        return pygame.Surface((width, height))

    def get_image(self, image):
        game_folder = os.path.dirname(__file__)
        img_folder = os.path.join(game_folder, 'img')
        return pygame.image.load(os.path.join(img_folder, image)).convert()

    def get_rect(self, x_border, y_border, width, height):
        return pygame.Rect(x_border, y_border, width, height)

    def get_keystate(self):
        keystate = pygame.key.get_pressed()
        # pylint: disable=no-member
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            return 'LEFT'
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            return 'RIGHT'
        if keystate[pygame.K_UP] or keystate[pygame.K_w]:
            return 'UP'
        if keystate[pygame.K_DOWN] or keystate[pygame.K_s]:
            return 'DOWN'
        # pylint: enable=no-member
        return None

    def get_events(self):
        return pygame.event.get()

    def get_event_type(self, event):
        # pylint: disable=no-member
        if event.type == pygame.QUIT:
            return 'QUIT'
        # pylint: enable=no-member
        return None

    def draw_line(self, screen, color, start, end):
        pygame.draw.line(screen, color, start, end)

    def flip_display(self):
        pygame.display.flip()

    def quit_game(self):
        # pylint: disable=no-member
        pygame.quit()
        # pylint: enable=no-member