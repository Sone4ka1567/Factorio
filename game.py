import sys
from player import Player, player_perks
from camera import Camera
from tree_sprite import Tree
from maps import EasyMapCreator, HardMapCreator
from core.virtual_objects.materials.raw_and_basics import Iron, Copper, Wood
from core.virtual_objects.materials.raw_and_basics import Coal, Stone, Silicon
import constants as const
import time

class Game:
    def __init__(self, gui):
        self.gui = gui
        self.gui.start()
        const.DISPLAY_W, const.DISPLAY_H = 1200, 864  # self.gui.get_display_info()
        self.screen = self.gui.set_screen(
            const.DISPLAY_W, const.DISPLAY_H,
            self.gui.get_hwsurface(), self.gui.get_double_buffer())

        self.gui.set_caption("ENDustrial")
        self.clock = self.gui.set_clock()

        self.big_font = self.gui.get_font("sylar_stencil.ttf", const.DISPLAY_H // 5)
        self.font = self.gui.get_font("sylar_stencil.ttf", const.DISPLAY_H // 7)
        self.small_font = self.gui.get_font("sylar_stencil.ttf", const.DISPLAY_H // 18)
        self.mini_font = self.gui.get_font("sylar_stencil.ttf", const.DISPLAY_H // 40)

        self.start_screen_playing = True
        self.choose_player_screen_playing, self.choose_map_playing = True, True
        self.choose_player_text, self.start_text, self.button_text = None, None, None
        self.player_perk, self.choose_map_text = None, None

    def new(self):
        self.all_sprites = self.gui.group_sprites()
        self.trees = self.gui.group_sprites()

        for i in range(const.MAP_W):
            for j in range(const.MAP_H):
                cur_cell = self.map_obj[self.map_matr[j][i]]
                if isinstance(cur_cell.raw_material_batch, Wood):
                    Tree(self, i, j, self.map_obj[self.map_matr[j][i]])

        self.player = Player(
            self, const.MAP_W // 2, const.MAP_H // 2, **player_perks[self.player_perk]
        )
        self.camera = Camera(const.PIXEL_MAP_W, const.PIXEL_MAP_H, self.gui)

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.gui.tick_fps(self.clock, const.FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        self.gui.quit_game()

    def update(self):
        self.gui.update_sprites(self.all_sprites)
        self.camera.update(self.player)

    def draw_map(self):

        if (self.player.rect.x - const.DISPLAY_W // 2) < const.PIXEL_MAP_W - const.DISPLAY_W:
            left_border = max(0, self.player.rect.x - const.DISPLAY_W // 2) // const.CELL_SIZE
        else:
            left_border = (const.PIXEL_MAP_W - const.DISPLAY_W) // const.CELL_SIZE

        if (self.player.rect.x + const.DISPLAY_W // 2) > const.DISPLAY_W:
            right_border = min(
                const.PIXEL_MAP_W,
                self.player.rect.x + const.DISPLAY_W // 2 + const.CELL_SIZE
            ) // const.CELL_SIZE
        else:
            right_border = const.DISPLAY_W // const.CELL_SIZE

        if (self.player.rect.y + const.DISPLAY_H // 2) > const.DISPLAY_H:
            bottom_border = min(
                const.PIXEL_MAP_H,
                self.player.rect.y + const.DISPLAY_H // 2 + const.CELL_SIZE
            ) // const.CELL_SIZE
        else:
            bottom_border = const.DISPLAY_H // const.CELL_SIZE

        if (self.player.rect.y - const.DISPLAY_H // 2) < const.PIXEL_MAP_H - const.DISPLAY_H:
            top_border = max(0, self.player.rect.y - const.DISPLAY_H // 2) // const.CELL_SIZE
        else:
            top_border = (const.PIXEL_MAP_H - const.DISPLAY_H) // const.CELL_SIZE

        for i in range(left_border, right_border):
            for j in range(top_border, bottom_border):

                cur_cell = self.map_obj[self.map_matr[j][i]]

                if cur_cell.category == "light":
                    cell_image = self.gui.get_image("dirt_and_ore/light_dirt.png").convert_alpha()
                else:
                    cell_image = self.gui.get_image("dirt_and_ore/dark_dirt.png").convert_alpha()

                # чек на руду
                if isinstance(cur_cell.raw_material_batch, Iron) \
                        and cur_cell.category == "light":
                    cell_image = self.gui.get_image(
                        "dirt_and_ore/light_dirt_with_iron.xcf"
                    ).convert_alpha()
                elif isinstance(cur_cell.raw_material_batch, Iron):
                    cell_image = self.gui.get_image(
                        "dirt_and_ore/dark_dirt_with_iron.xcf"
                    ).convert_alpha()

                if isinstance(cur_cell.raw_material_batch, Copper) \
                        and cur_cell.category == "light":
                    cell_image = self.gui.get_image(
                        "dirt_and_ore/light_dirt_with_copper.xcf"
                    ).convert_alpha()
                elif isinstance(cur_cell.raw_material_batch, Copper):
                    cell_image = self.gui.get_image(
                        "dirt_and_ore/dark_dirt_with_copper.xcf"
                    ).convert_alpha()

                if isinstance(cur_cell.raw_material_batch, Coal) \
                        and cur_cell.category == "light":
                    cell_image = self.gui.get_image(
                        "dirt_and_ore/light_dirt_with_coal.xcf"
                    ).convert_alpha()
                elif isinstance(cur_cell.raw_material_batch, Coal):
                    cell_image = self.gui.get_image(
                        "dirt_and_ore/dark_dirt_with_coal.xcf"
                    ).convert_alpha()

                if isinstance(cur_cell.raw_material_batch, Stone) \
                        and cur_cell.category == "light":
                    cell_image = self.gui.get_image(
                        "dirt_and_ore/light_dirt_with_stone.xcf"
                    ).convert_alpha()
                elif isinstance(cur_cell.raw_material_batch, Stone):
                    cell_image = self.gui.get_image(
                        "dirt_and_ore/dark_dirt_with_stone.xcf"
                    ).convert_alpha()

                if isinstance(cur_cell.raw_material_batch, Silicon) \
                        and cur_cell.category == "light":
                    cell_image = self.gui.get_image(
                        "dirt_and_ore/light_dirt_with_silicon.xcf"
                    ).convert_alpha()
                elif isinstance(cur_cell.raw_material_batch, Silicon):
                    cell_image = self.gui.get_image(
                        "dirt_and_ore/dark_dirt_with_silicon.xcf"
                    ).convert_alpha()

                if isinstance(cur_cell.raw_material_batch, Wood) \
                        and cur_cell.category == "light":
                    cell_image = self.gui.get_image(
                        "dirt_and_ore/light_dirt.png"
                    ).convert_alpha()
                elif isinstance(cur_cell.raw_material_batch, Wood):
                    cell_image = self.gui.get_image(
                        "dirt_and_ore/dark_dirt.png"
                    ).convert_alpha()

                self.screen.blit(cell_image,
                                 ((i - left_border) * const.CELL_SIZE, (j - top_border) * const.CELL_SIZE))

    def draw(self):
        self.gui.fill_screen(self.screen, const.BG_COLOR)
        self.draw_map()

        mouse = self.gui.get_mouse_pos()
        x_coord = mouse[0] // const.CELL_SIZE
        y_coord = mouse[1] // const.CELL_SIZE
        x_coord *= const.CELL_SIZE
        y_coord *= const.CELL_SIZE
        self.gui.draw_line(self.screen, const.HIGHLIGHT, (x_coord, y_coord), (x_coord + const.CELL_SIZE, y_coord))
        self.gui.draw_line(self.screen, const.HIGHLIGHT, (x_coord, y_coord), (x_coord, y_coord + const.CELL_SIZE))
        self.gui.draw_line(self.screen, const.HIGHLIGHT, (x_coord + const.CELL_SIZE, y_coord),
                           (x_coord + const.CELL_SIZE, y_coord + const.CELL_SIZE))
        self.gui.draw_line(self.screen, const.HIGHLIGHT, (x_coord, y_coord + const.CELL_SIZE),
                           (x_coord + const.CELL_SIZE, y_coord + const.CELL_SIZE))

        for sprite in self.all_sprites:
            if sprite.category == 'tree' and not sprite.map_obj.raw_material_batch:
                sprite.change_image()
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        self.gui.flip_display()

    def events(self):
        for event in self.gui.get_events():
            if self.gui.get_event_type(event) == 'MOUSEBUTTONDOWN' and event.button == 3:

                if (self.player.rect.x - const.DISPLAY_W // 2) < const.PIXEL_MAP_W - const.DISPLAY_W:
                    left_border = max(0, self.player.rect.x - const.DISPLAY_W // 2) // const.CELL_SIZE
                else:
                    left_border = (const.PIXEL_MAP_W - const.DISPLAY_W) // const.CELL_SIZE

                if (self.player.rect.y - const.DISPLAY_H // 2) < const.PIXEL_MAP_H - const.DISPLAY_H:
                    top_border = max(0, self.player.rect.y - const.DISPLAY_H // 2) // const.CELL_SIZE
                else:
                    top_border = (const.PIXEL_MAP_H - const.DISPLAY_H) // const.CELL_SIZE

                i_ind = event.pos[0] // const.CELL_SIZE + left_border
                j_ind = event.pos[1] // const.CELL_SIZE + top_border
                message = self.player.dig(self.map_obj[self.map_matr[j_ind][i_ind]])

                if message['message'] == 'bag is full' or message['message'] == 'nothing to dig here':
                    color = const.RED
                else:
                    color = const.WHITE
                button_text = self.mini_font.render(message['message'], True, color)
                self.screen.blit(button_text, (event.pos[0], event.pos[1] - const.CELL_SIZE // 2))
                self.gui.update_display()
                time.sleep(0.3)
                self.gui.tick_fps(self.clock, const.FPS)

            if 'E' in self.gui.get_keystate():
                self.show_bag()

            if self.gui.get_event_type(event) == "QUIT":
                self.quit()

    def show_bag(self):
        self.show_bag_playing = True

        while self.show_bag_playing:
            self.screen.fill(const.BAGCOLOR)
            text_left = self.small_font.render('Character', True, const.WHITE)
            text_right = self.small_font.render('Crafting', True,  const.WHITE)

            self.gui.draw_line(self.screen, const.BLACK,
                               (const.DISPLAY_W // 2, 0), (const.DISPLAY_W // 2, const.DISPLAY_H))
            self.screen.blit(text_left,
                             (const.DISPLAY_W // 20, const.DISPLAY_H // 20))
            self.screen.blit(text_right,
                             (const.DISPLAY_W // 2 + const.DISPLAY_W // 20, const.DISPLAY_H // 20))

            for event in self.gui.get_events():
                if self.gui.get_event_type(event) == "QUIT":
                    self.quit()

                if 'ESCAPE' in self.gui.get_keystate():
                    self.show_bag_playing = False

            self.gui.update_display()
            self.gui.tick_fps(self.clock, const.FPS)

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
        self.start_text = self.big_font.render("ENDustrial", True, const.ORANGE_GREY)

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
