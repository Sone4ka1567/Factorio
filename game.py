from pygameGUI import PygameGUI
from player import Player, player_perks
from camera import Camera
from constants import *


class Game:
    def __init__(self):
        self.gui = PygameGUI()
        self.gui.start()
        self.screen = self.gui.set_screen(DISPLAY_W, DISPLAY_H)
        self.gui.set_caption('ENDustrial')
        self.clock = self.gui.set_clock()

    def load_map(self):  # TODO
        pass
        '''
        folder = path.dirname(__file__)
        map_generator(self.difficulty, self.difficulty)
        self.map = Map(path.join(folder, 'map.txt'))
        '''

    def new(self):
        self.load_map()
        self.all_sprites = self.gui.group_sprites()
        # здесь надо будет еще обработать карту
        self.player = Player(self, 0, 0, **player_perks['fast'])
        # self.camera = Camera(self.map.width, self.map.height)
        self.camera = Camera(PIXEL_MAP_W, PIXEL_MAP_H)

    def run(self):
        self.playing = True
        while self.playing:
            self.gui.set_fps(self.clock, FPS)
            self.events()
            self.update()
            self.draw()

    def quit(self):
        self.gui.quit_game()

    def update(self):
        self.gui.update_sprites(self.all_sprites)
        self.camera.update(self.player)

    def draw_grid(self):
        for x in range(0, DISPLAY_W, CELL_SIZE):
            self.gui.draw_line(self.screen, WHITE, (x, 0), (x, DISPLAY_H))
        for y in range(0, DISPLAY_H, CELL_SIZE):
            self.gui.draw_line(self.screen, WHITE, (0, y), (DISPLAY_W, y))

    def draw(self):
        self.gui.fill_screen(self.screen, BG_COLOR)
        self.draw_grid()

        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        self.gui.flip_display()

    def events(self):
        for event in self.gui.get_events():
            if self.gui.get_event_type(event) == 'QUIT':
                self.playing = False

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass
