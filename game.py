import sys
from pygamegui import PygameGUI
from player import Player, player_perks
from camera import Camera
from maps import EasyMapCreator, HardMapCreator
from core.virtual_objects.materials.raw_and_basics import Iron, Copper, Wood
from core.virtual_objects.materials.raw_and_basics import Coal, Stone, Silicon
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

    def new(self):
        # self.load_map()
        self.all_sprites = self.gui.group_sprites()
        # здесь надо будет еще обработать карту
        self.player = Player(
            self, const.MAP_W // 2, const.MAP_H // 2, **player_perks[self.player_perk]
        )
        self.camera = Camera(const.PIXEL_MAP_W, const.PIXEL_MAP_H)

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.gui.tick_fps(self.clock, const.FPS) / 500
            self.events()
            self.update()
            self.draw()

    def quit(self):
        self.gui.quit_game()

    def update(self):
        self.gui.update_sprites(self.all_sprites)
        self.camera.update(self.player)

    def draw_map(self):
        x_cell = self.player.rect.x // const.CELL_SIZE
        y_cell = self.player.rect.y // const.CELL_SIZE
        cell_left = x_cell - self.screen.get_width() // const.CELL_SIZE
        cell_right = x_cell + self.screen.get_width() // const.CELL_SIZE
        cell_top = y_cell - self.screen.get_height() // const.CELL_SIZE
        cell_bottom = y_cell + self.screen.get_height() // const.CELL_SIZE

        # проверим на границы
        cell_left = max(0, cell_left)
        cell_right = min(const.MAP_W - 1, cell_right)
        cell_top = max(0, cell_top)
        cell_bottom = min(const.MAP_H - 1, cell_bottom)

        for i in range(cell_left, cell_right + 1):
            for j in range(cell_top, cell_bottom + 1):

                cur_cell = self.map_obj[self.map_matr[j][i]]

                if cur_cell.category == "light":
                    cell_image = self.gui.get_image("dirt_and_ore/light_dirt.png")
                else:
                    cell_image = self.gui.get_image("dirt_and_ore/dark_dirt.png")

                # чек на руду
                if isinstance(cur_cell.raw_material_batch, Iron) \
                        and cur_cell.category == "light":
                    cell_image = self.gui.get_image("dirt_and_ore/light_dirt_with_iron.xcf")
                elif isinstance(cur_cell.raw_material_batch, Iron):
                    cell_image = self.gui.get_image("dirt_and_ore/dark_dirt_with_iron.xcf")

                if isinstance(cur_cell.raw_material_batch, Copper) \
                        and cur_cell.category == "light":
                    cell_batch_image = self.gui.get_image("dirt_and_ore/light_dirt_with_copper.xcf")
                elif isinstance(cur_cell.raw_material_batch, Copper):
                    cell_batch_image = self.gui.get_image("dirt_and_ore/dark_dirt_with_copper.xcf")

                if isinstance(cur_cell.raw_material_batch, Coal) \
                        and cur_cell.category == "light":
                    cell_image = self.gui.get_image("dirt_and_ore/light_dirt_with_coal.xcf")
                elif isinstance(cur_cell.raw_material_batch, Coal):
                    cell_image = self.gui.get_image("dirt_and_ore/dark_dirt_with_coal.xcf")

                if isinstance(cur_cell.raw_material_batch, Stone) \
                        and cur_cell.category == "light":
                    cell_image = self.gui.get_image("dirt_and_ore/light_dirt_with_stone.xcf")
                elif isinstance(cur_cell.raw_material_batch, Stone):
                    cell_image = self.gui.get_image("dirt_and_ore/dark_dirt_with_stone.xcf")

                if isinstance(cur_cell.raw_material_batch, Silicon) \
                        and cur_cell.category == "light":
                    cell_image = self.gui.get_image("dirt_and_ore/light_dirt_with_silicon.xcf")
                elif isinstance(cur_cell.raw_material_batch, Silicon):
                    cell_image = self.gui.get_image("dirt_and_ore/dark_dirt_with_silicon.xcf")

                if isinstance(cur_cell.raw_material_batch, Wood) \
                        and cur_cell.category == "light":
                    cell_image = self.gui.get_image("dirt_and_ore/light_dirt_with_tree.xcf")
                elif isinstance(cur_cell.raw_material_batch, Wood):
                    cell_image = self.gui.get_image("dirt_and_ore/dark_dirt_with_tree.xcf")

                self.screen.blit(cell_image,
                                 ((i - cell_left) * const.CELL_SIZE, (j - cell_top) * const.CELL_SIZE))

    def draw(self):
        self.gui.fill_screen(self.screen, const.BG_COLOR)
        self.draw_map()
        # self.gui.update_display()

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
                        if level == "easy":
                            creator = EasyMapCreator()
                        else:
                            creator = HardMapCreator()
                        self.map = creator.gen_map()
                        self.map_matr = self.map.get_map_matrix()
                        self.map_obj = self.map.get_map_objects()
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
            self.gui.tick_fps(self.clock, const.FPS)

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
            self.gui.tick_fps(self.clock, const.FPS)

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
            self.gui.tick_fps(self.clock, const.FPS)

    def show_go_screen(self):
        pass
