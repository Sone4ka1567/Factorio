from pygamegui import PygameGUI
from player import Player, player_perks
from camera import Camera
import constants as const


class Game:
    def __init__(self):
        self.gui = PygameGUI()
        self.gui.start()
        const.DISPLAY_W, const.DISPLAY_H = self.gui.get_display_info()
        self.screen = self.gui.set_screen(const.DISPLAY_W, const.DISPLAY_H)
        self.gui.set_caption('ENDustrial')
        self.clock = self.gui.set_clock()

    '''
     def load_map(self):
        folder = path.dirname(__file__)
        map_generator(self.difficulty, self.difficulty)
        self.map = Map(path.join(folder, 'map.txt')) 
        '''

    def new(self):
        # self.load_map()
        self.all_sprites = self.gui.group_sprites()
        # здесь надо будет еще обработать карту
        self.player = Player(self, 0, 0, **player_perks['fast'])
        # self.camera = Camera(self.map.width, self.map.height)
        self.camera = Camera(const.PIXEL_MAP_W, const.PIXEL_MAP_H)

    def run(self):
        self.playing = True
        while self.playing:
            self.gui.set_fps(self.clock, const.FPS)
            self.events()
            self.update()
            self.draw()

    def quit(self):
        self.gui.quit_game()

    def update(self):
        self.gui.update_sprites(self.all_sprites)
        self.camera.update(self.player)

    def draw_grid(self):
        for x_border in range(0, const.DISPLAY_W, const.CELL_SIZE):
            self.gui.draw_line(self.screen, const.WHITE, (x_border, 0), (x_border, const.DISPLAY_H))
        for y_border in range(0, const.DISPLAY_H, const.CELL_SIZE):
            self.gui.draw_line(self.screen, const.WHITE, (0, y_border), (const.DISPLAY_W, y_border))

    def draw(self):
        self.gui.fill_screen(self.screen, const.BG_COLOR)
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
