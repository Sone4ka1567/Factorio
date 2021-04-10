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
        self.gui.set_caption("ENDustrial")
        self.clock = self.gui.set_clock()

        self.big_font = self.gui.get_font("comicsansms", 350)
        self.font = self.gui.get_font("comicsansms", 150)
        self.small_font = self.gui.get_font("comicsansms", 100)

        self.start_screen_playing = True

    """
     def load_map(self):
        folder = path.dirname(__file__)
        map_generator(self.difficulty, self.difficulty)
        self.map = Map(path.join(folder, 'map.txt')) 
        """

    def new(self):
        # self.load_map()
        self.all_sprites = self.gui.group_sprites()
        # здесь надо будет еще обработать карту
        self.player = Player(self, 0, 0, **player_perks["fast"])
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
            self.gui.draw_line(
                self.screen, const.WHITE, (x_border, 0), (x_border, const.DISPLAY_H)
            )
        for y_border in range(0, const.DISPLAY_H, const.CELL_SIZE):
            self.gui.draw_line(
                self.screen, const.WHITE, (0, y_border), (const.DISPLAY_W, y_border)
            )

    def draw(self):
        self.gui.fill_screen(self.screen, const.BG_COLOR)
        self.draw_grid()

        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        self.gui.flip_display()

    def events(self):
        for event in self.gui.get_events():
            if self.gui.get_event_type(event) == "QUIT":
                self.quit()

    def create_button(self, message, x_left, y_top, width, height, hover_color, default_color, level):
        mouse = self.gui.get_mouse_pos()
        click = self.gui.get_mouse_pressed()
        if x_left + width > mouse[0] > x_left and y_top + height > mouse[1] > y_top:
            self.gui.draw_rect(self.screen, hover_color, (x_left, y_top, width, height))
            if click[0] == 1:
                if level == 'start':
                    self.start_screen_playing = False
        else:
            self.gui.draw_rect(self.screen, default_color, (x_left, y_top, width, height))

        self.button_text = self.small_font.render(message, True, const.BLACK)
        self.screen.blit(self.button_text, (x_left + (width - self.button_text.get_width()) / 2,
                                            y_top + (height - self.button_text.get_height()) / 2))

    def show_start_screen(self):
        self.start_text = self.big_font.render("ENDustrial", True, const.ORANGE_GREY)

        while self.start_screen_playing:
            self.screen.fill(const.BG_COLOR)
            self.screen.blit(self.start_text,
                             ((const.DISPLAY_W - self.start_text.get_width()) / 2, const.DISPLAY_H // 6))

            self.create_button("LET'S GO", const.DISPLAY_W / 2 - const.DISPLAY_W // 10, const.DISPLAY_H / 2,
                               const.DISPLAY_W // 5, const.DISPLAY_H // 8, const.WHITE, const.LIGHT_GREY, 'start')

            self.events()

            self.gui.update_display()
            self.gui.set_fps(self.clock, const.FPS)

    def show_go_screen(self):
        pass
