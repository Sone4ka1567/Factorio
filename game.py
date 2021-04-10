import sys
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

        self.big_font = self.gui.get_font("sylar_stencil.ttf", const.DISPLAY_H // 4)
        self.font = self.gui.get_font("sylar_stencil.ttf", const.DISPLAY_H // 6)
        self.small_font = self.gui.get_font("sylar_stencil.ttf", const.DISPLAY_H // 16)

        self.start_screen_playing = True
        self.choose_player_screen_playing, self.choose_map_playing = True, True
        self.choose_player_text, self.start_text, self.button_text = None, None, None
        self.player_perk, self.choose_map_text = None, None

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
        self.player = Player(self, 0, 0, **player_perks[self.player_perk])
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

    def create_button(
        self, message, x_left, y_top, width, height, hovercolor, defaultcolor, level
    ):
        mouse = self.gui.get_mouse_pos()
        if x_left + width > mouse[0] > x_left and y_top + height > mouse[1] > y_top:
            self.gui.draw_rect(self.screen, hovercolor, (x_left, y_top, width, height))
            for event in self.gui.get_events():
                if self.gui.get_event_type(event) == "MOUSEBUTTONDOWN":
                    if level == "start":
                        self.start_screen_playing = False
                    elif level == "exit":
                        self.quit()
                        sys.exit()
                    elif level in ("fast", "balanced", "big_bag"):
                        self.player_perk = level
                        self.choose_player_screen_playing = False
                    elif level in ("easy", "hard"):
                        if level == "easy":  #TODO
                            pass
                        else:
                            pass
                        self.choose_map_playing = False
        else:
            self.gui.draw_rect(
                self.screen, defaultcolor, (x_left, y_top, width, height)
            )

        self.button_text = self.small_font.render(message, True, const.BLACK)
        self.screen.blit(
            self.button_text,
            (
                x_left + (width - self.button_text.get_width()) / 2,
                y_top + (height - self.button_text.get_height()) / 2,
            ),
        )

    def show_start_screen(self):
        self.start_text = self.font.render("ENDustrial", True, const.ORANGE_GREY)

        while self.start_screen_playing:
            self.screen.fill(const.BG_COLOR)
            self.screen.blit(
                self.start_text,
                (
                    (const.DISPLAY_W - self.start_text.get_width()) / 2,
                    const.DISPLAY_H // 8,
                ),
            )

            self.create_button(
                "START",
                const.DISPLAY_W / 2 - const.DISPLAY_W // 12,
                const.DISPLAY_H / 2,
                const.DISPLAY_W // 6,
                const.DISPLAY_H // 12,
                const.WHITE,
                const.ORANGE_GREY,
                "start",
            )

            self.create_button(
                "CREDITS",
                const.DISPLAY_W / 2 - const.DISPLAY_W // 12,
                const.DISPLAY_H / 2 + const.DISPLAY_H // 6,
                const.DISPLAY_W // 6,
                const.DISPLAY_H // 12,
                const.WHITE,
                const.ORANGE_GREY,
                "credits",
            )

            self.create_button(
                "EXIT",
                const.DISPLAY_W / 2 - const.DISPLAY_W // 12,
                const.DISPLAY_H / 2 + const.DISPLAY_H // 3,
                const.DISPLAY_W // 6,
                const.DISPLAY_H // 12,
                const.WHITE,
                const.ORANGE_GREY,
                "exit",
            )

            self.events()

            self.gui.update_display()
            self.gui.set_fps(self.clock, const.FPS)

    def choose_player_screen(self):
        self.choose_player_text = self.font.render(
            "Choose a player", True, const.ORANGE_GREY
        )

        while self.choose_player_screen_playing:
            self.screen.fill(const.BG_COLOR)
            self.screen.blit(
                self.choose_player_text,
                (
                    (const.DISPLAY_W - self.choose_player_text.get_width()) / 2,
                    const.DISPLAY_H // 8,
                ),
            )

            self.create_button(
                "FAST",
                const.DISPLAY_W / 2 - const.DISPLAY_W // 10,
                const.DISPLAY_H / 2,
                const.DISPLAY_W // 5,
                const.DISPLAY_H // 12,
                const.WHITE,
                const.ORANGE_GREY,
                "fast",
            )

            self.create_button(
                "BALANCED",
                const.DISPLAY_W / 2 - const.DISPLAY_W // 10,
                const.DISPLAY_H / 2 + const.DISPLAY_H // 6,
                const.DISPLAY_W // 5,
                const.DISPLAY_H // 12,
                const.WHITE,
                const.ORANGE_GREY,
                "balanced",
            )

            self.create_button(
                "BIG BAG",
                const.DISPLAY_W / 2 - const.DISPLAY_W // 10,
                const.DISPLAY_H / 2 + const.DISPLAY_H // 3,
                const.DISPLAY_W // 5,
                const.DISPLAY_H // 12,
                const.WHITE,
                const.ORANGE_GREY,
                "big_bag",
            )

            self.events()

            self.gui.update_display()
            self.gui.set_fps(self.clock, const.FPS)

    def choose_map_screen(self):
        self.choose_map_text = self.font.render(
            "Choose difficulty", True, const.ORANGE_GREY
        )

        while self.choose_map_playing:
            self.screen.fill(const.BG_COLOR)
            self.screen.blit(
                self.choose_map_text,
                (
                    (const.DISPLAY_W - self.choose_map_text.get_width()) / 2,
                    const.DISPLAY_H // 8,
                ),
            )

            self.create_button(
                "EASY",
                const.DISPLAY_W / 2 - const.DISPLAY_W // 10,
                const.DISPLAY_H / 2,
                const.DISPLAY_W // 5,
                const.DISPLAY_H // 12,
                const.WHITE,
                const.ORANGE_GREY,
                "easy",
            )

            self.create_button(
                "HARD",
                const.DISPLAY_W / 2 - const.DISPLAY_W // 10,
                const.DISPLAY_H / 2 + const.DISPLAY_H // 6,
                const.DISPLAY_W // 5,
                const.DISPLAY_H // 12,
                const.WHITE,
                const.ORANGE_GREY,
                "hard",
            )

            self.events()

            self.gui.update_display()
            self.gui.set_fps(self.clock, const.FPS)

    def show_go_screen(self):
        pass
