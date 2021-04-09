from facade import GUI
import pygame
import os


class PygameSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.speedx = 0
        self.speedy = 0
        self.gui = PygameGUI()

    def init_sprite_and_group(self, group):
        pygame.sprite.Sprite.__init__(self, group)


class PygameGUI(GUI):
    def __init__(self):
        super().__init__()

    def start(self):
        pygame.init()

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

    def get_rect(self, x, y, width, height):
        return pygame.Rect(x, y, width, height)


    def get_keystate(self):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            return 'LEFT'
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            return 'RIGHT'
        if keystate[pygame.K_UP] or keystate[pygame.K_w]:
            return 'UP'
        if keystate[pygame.K_DOWN] or keystate[pygame.K_s]:
            return 'DOWN'

    def get_events(self):
        return pygame.event.get()

    def get_event_type(self, event):
        if event.type == pygame.QUIT:
            return 'QUIT'

    def draw_line(self, screen, color, start, end):
        pygame.draw.line(screen, color, start, end)

    def flip_display(self):
        pygame.display.flip()

    def quit_game(self):
        pygame.quit()
