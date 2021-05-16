import sys
from player import Player, player_perks
from camera import Camera
from tree_sprite import Tree
from maps import EasyMapCreator, HardMapCreator, EasyMap, HardMap
from core.virtual_objects.materials.raw_and_basics import Iron, Copper, Wood
from core.virtual_objects.materials.raw_and_basics import Coal, Stone, Silicon
from basic_geometry import euclidean_dist
import constants as const
import time
import json


class Game:
    def __init__(self, gui):
        self.gui = gui
        self.gui.start()
        const.DISPLAY_W, const.DISPLAY_H = 1408, 864  # self.gui.get_display_info()
        self.screen = self.gui.set_screen(
            const.DISPLAY_W, const.DISPLAY_H,
            self.gui.get_hwsurface(), self.gui.get_double_buffer())

        self.gui.set_caption("ENDustrial")
        self.clock = self.gui.set_clock()
        # self.gui.set_music('sounds/welcome_music.wav') todo

        self.big_font = self.gui.get_font("fonts/sylar_stencil.ttf", const.DISPLAY_H // 5)
        self.font = self.gui.get_font("fonts/sylar_stencil.ttf", const.DISPLAY_H // 7)
        self.small_font = self.gui.get_font("fonts/sylar_stencil.ttf", const.DISPLAY_H // 18)
        self.mini_font = self.gui.get_font("fonts/sylar_stencil.ttf", const.DISPLAY_H // 40)
        self.additional_mini_font = self.gui.get_font("fonts/Roboto-Bold.ttf", const.DISPLAY_H // 40)

        self.start_screen_playing = True
        self.choose_player_screen_playing, self.choose_map_playing = True, True
        self.choose_player_text, self.start_text, self.button_text = None, None, None
        self.player_perk, self.choose_map_text = None, None

    def new(self):
        # self.gui.stop_music() todo
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

        if (self.player.rect.x - const.DISPLAY_W // 2) < const.PIXEL_MAP_W - const.DISPLAY_W:
            left_border = max(0, self.player.rect.x - const.DISPLAY_W // 2) // const.CELL_SIZE
        else:
            left_border = (const.PIXEL_MAP_W - const.DISPLAY_W) // const.CELL_SIZE

        if (self.player.rect.y - const.DISPLAY_H // 2) < const.PIXEL_MAP_H - const.DISPLAY_H:
            top_border = max(0, self.player.rect.y - const.DISPLAY_H // 2) // const.CELL_SIZE
        else:
            top_border = (const.PIXEL_MAP_H - const.DISPLAY_H) // const.CELL_SIZE

        i_ind = mouse[0] // const.CELL_SIZE + left_border
        j_ind = mouse[1] // const.CELL_SIZE + top_border
        cur_cell = self.map_obj[self.map_matr[j_ind][i_ind]]
        if cur_cell.raw_material_batch:
            message = str(cur_cell.raw_material_batch)
            text = self.additional_mini_font.render(message, True, const.WHITE)
            self.gui.draw_rect(
                self.screen, const.BAGCOLOR,
                (const.DISPLAY_W - const.CELL_SIZE * 3, 0,
                 const.CELL_SIZE * 3, const.CELL_SIZE * 2)
            )
            cell_image = self.gui.get_image(
                cur_cell.raw_material_batch.get_icon_path()
            ).convert_alpha()
            cell_image.set_colorkey(const.BLACK)

            self.screen.blit(cell_image, ((const.DISPLAY_W - const.CELL_SIZE * 3) +
                                          (const.CELL_SIZE * 3 - cell_image.get_width()) / 2, const.CELL_SIZE * 0.25))
            self.screen.blit(text, ((const.DISPLAY_W - const.CELL_SIZE * 3) +
                                    (const.CELL_SIZE * 3 - text.get_width()) / 2, const.CELL_SIZE * 1.25))

        self.gui.flip_display()

    def show_message(self, text, color, event):
        button_text = self.additional_mini_font.render(text, True, color)
        self.screen.blit(button_text, (event.pos[0], event.pos[1] - const.CELL_SIZE // 2))
        self.gui.update_display()
        time.sleep(0.3)
        self.gui.tick_fps(self.clock, const.FPS)

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

                if euclidean_dist(i_ind - self.player.rect.x // const.CELL_SIZE,
                                  j_ind - self.player.rect.y // const.CELL_SIZE) < 5:
                    message = self.player.dig(self.map_obj[self.map_matr[j_ind][i_ind]])
                    color = const.WHITE if message['ok'] else const.RED
                    self.show_message(message['message'], color, event)
                else:
                    self.show_message('too far, come closer', const.RED, event)

            if 'E' in self.gui.get_keystate():
                self.show_bag()

            if self.gui.get_event_type(event) == "QUIT":
                self.quit()

    def show_bag(self):
        self.show_bag_playing = True
        self.module_playing = 'production'

        while self.show_bag_playing:
            self.screen.fill(const.BAGCOLOR)
            text_left = self.small_font.render('Character', True, const.WHITE)
            text_right = self.small_font.render('Crafting', True, const.WHITE)

            self.gui.draw_line(self.screen, const.BLACK,
                               (const.DISPLAY_W // 2, 0), (const.DISPLAY_W // 2, const.DISPLAY_H))
            self.screen.blit(text_left,
                             (const.DISPLAY_W // 20, const.DISPLAY_H // 20))
            self.screen.blit(text_right,
                             (const.DISPLAY_W // 2 + const.DISPLAY_W // 20, const.DISPLAY_H // 20))

            # LEFT SIDE

            y_start = const.DISPLAY_H // 6
            x_start = const.DISPLAY_W // 20
            for i in range((self.player.bag_capacity + 5) // 5):
                for j in range(5):
                    if i * 5 + j >= self.player.bag_capacity:
                        break
                    self.gui.draw_rect(
                        self.screen, const.LIGHT_GREY,
                        (x_start + j * 2 * const.CELL_SIZE, y_start + i * 2 * const.CELL_SIZE,
                         const.CELL_SIZE, const.CELL_SIZE)
                    )

            batches = self.player.bag.get_data()
            for x in range(len(batches)):
                i_ind = x // 5
                j_ind = x % 5

                cell_image = self.gui.get_image(
                    batches[x].get_icon_path()
                ).convert_alpha()

                cell_image.set_colorkey(const.BLACK)

                self.screen.blit(cell_image,
                                 (x_start + j_ind * 2 * const.CELL_SIZE, y_start + i_ind * 2 * const.CELL_SIZE))

                batch_amount = self.additional_mini_font.render(str(batches[x].amount), True, const.WHITE)
                self.screen.blit(
                    batch_amount,
                    (
                        x_start + j_ind * 2 * const.CELL_SIZE + const.CELL_SIZE - batch_amount.get_width(),
                        y_start + i_ind * 2 * const.CELL_SIZE + const.CELL_SIZE // 2,
                    ),
                )

            # RIGHT SIDE

            y_start = const.DISPLAY_H // 6
            x_start = const.DISPLAY_W // 20 + const.DISPLAY_W // 2
            production_image = self.gui.get_image('icons/modules/production.png').convert_alpha()
            production_image.set_colorkey(const.BLACK)
            inter_products_image = self.gui.get_image('icons/modules/intermediate-products.png').convert_alpha()
            inter_products_image.set_colorkey(const.BLACK)
            logistics_image = self.gui.get_image('icons/modules/logistics.png').convert_alpha()
            logistics_image.set_colorkey(const.BLACK)

            production_color = const.LIGHT_GREY
            logistics_color = const.LIGHT_GREY
            inter_products_color = const.LIGHT_GREY

            sub_y_start = y_start + 3 * const.CELL_SIZE

            if self.module_playing == 'production':
                production_color = const.ORANGE_GREY

                img = self.gui.get_image('icons/creators/production/burner-mining-drill.png').convert_alpha()
                self.draw_icon(const.LIGHT_GREY, x_start, sub_y_start,
                               const.CELL_SIZE, const.CELL_SIZE, img)

                img = self.gui.get_image('icons/creators/production/electric-mining-drill.png').convert_alpha()
                self.draw_icon(const.LIGHT_GREY, x_start + 2 * const.CELL_SIZE, sub_y_start,
                               const.CELL_SIZE, const.CELL_SIZE, img)

                img = self.gui.get_image('icons/creators/production/assembling-machine-1.png').convert_alpha()
                self.draw_icon(const.LIGHT_GREY, x_start, sub_y_start + 2 * const.CELL_SIZE,
                               const.CELL_SIZE, const.CELL_SIZE, img)

                img = self.gui.get_image('icons/creators/production/assembling-machine-2.png').convert_alpha()
                self.draw_icon(const.LIGHT_GREY, x_start + 2 * const.CELL_SIZE, sub_y_start + 2 * const.CELL_SIZE,
                               const.CELL_SIZE, const.CELL_SIZE, img)

                img = self.gui.get_image('icons/creators/production/electric-furnace.png').convert_alpha()
                self.draw_icon(const.LIGHT_GREY, x_start, sub_y_start + 4 * const.CELL_SIZE,
                               const.CELL_SIZE, const.CELL_SIZE, img)

                img = self.gui.get_image('icons/creators/production/stone-furnace.png').convert_alpha()
                self.draw_icon(const.LIGHT_GREY, x_start + 2 * const.CELL_SIZE, sub_y_start + 4 * const.CELL_SIZE,
                               const.CELL_SIZE, const.CELL_SIZE, img)

                img = self.gui.get_image('icons/radar.png').convert_alpha()
                self.draw_icon(const.LIGHT_GREY, x_start, sub_y_start + 6 * const.CELL_SIZE,
                               const.CELL_SIZE, const.CELL_SIZE, img)

            elif self.module_playing == 'logistics':
                logistics_color = const.ORANGE_GREY

                img = self.gui.get_image('icons/creators/electricity/small-electric-pole.png').convert_alpha()
                self.draw_icon(const.LIGHT_GREY, x_start, sub_y_start,
                               const.CELL_SIZE, const.CELL_SIZE, img)

                img = self.gui.get_image('icons/creators/electricity/big-electric-pole.png').convert_alpha()
                self.draw_icon(const.LIGHT_GREY, x_start + 2 * const.CELL_SIZE, sub_y_start,
                               const.CELL_SIZE, const.CELL_SIZE, img)

                img = self.gui.get_image('icons/creators/electricity/burner-generator.xcf').convert_alpha()
                self.draw_icon(const.LIGHT_GREY, x_start, sub_y_start + 2 * const.CELL_SIZE,
                               const.CELL_SIZE, const.CELL_SIZE, img)

            else:
                inter_products_color = const.ORANGE_GREY

                img = self.gui.get_image('icons/materials/intermediate/copper-cable.png').convert_alpha()
                self.draw_icon(const.LIGHT_GREY, x_start, sub_y_start,
                               const.CELL_SIZE, const.CELL_SIZE, img)

                img = self.gui.get_image('icons/materials/intermediate/steel-plate.png').convert_alpha()
                self.draw_icon(const.LIGHT_GREY, x_start + 2 * const.CELL_SIZE, sub_y_start,
                               const.CELL_SIZE, const.CELL_SIZE, img)

                img = self.gui.get_image('icons/materials/intermediate/pipe.png').convert_alpha()
                self.draw_icon(const.LIGHT_GREY, x_start + 4 * const.CELL_SIZE, sub_y_start,
                               const.CELL_SIZE, const.CELL_SIZE, img)

                img = self.gui.get_image('icons/materials/intermediate/iron-gear-wheel.png').convert_alpha()
                self.draw_icon(const.LIGHT_GREY, x_start, sub_y_start + 2 * const.CELL_SIZE,
                               const.CELL_SIZE, const.CELL_SIZE, img)

                img = self.gui.get_image('icons/materials/intermediate/electric-circuit.png').convert_alpha()
                self.draw_icon(const.LIGHT_GREY, x_start + 2 * const.CELL_SIZE, sub_y_start + 2 * const.CELL_SIZE,
                               const.CELL_SIZE, const.CELL_SIZE, img)

                img = self.gui.get_image('icons/materials/intermediate/resistor.xcf').convert_alpha()
                self.draw_icon(const.LIGHT_GREY, x_start + 4 * const.CELL_SIZE, sub_y_start + 2 * const.CELL_SIZE,
                               const.CELL_SIZE, const.CELL_SIZE, img)

                img = self.gui.get_image('icons/materials/intermediate/transistor.xcf').convert_alpha()
                self.draw_icon(const.LIGHT_GREY, x_start, sub_y_start + 4 * const.CELL_SIZE,
                               const.CELL_SIZE, const.CELL_SIZE, img)

                img = self.gui.get_image('icons/materials/intermediate/integrated-circuit.png').convert_alpha()
                self.draw_icon(const.LIGHT_GREY, x_start + 2 * const.CELL_SIZE, sub_y_start + 4 * const.CELL_SIZE,
                               const.CELL_SIZE, const.CELL_SIZE, img)

                img = self.gui.get_image('icons/materials/intermediate/control-unit.png').convert_alpha()
                self.draw_icon(const.LIGHT_GREY, x_start + 4 * const.CELL_SIZE, sub_y_start + 4 * const.CELL_SIZE,
                               const.CELL_SIZE, const.CELL_SIZE, img)

            self.gui.draw_rect(  # production
                self.screen, production_color,
                (x_start, y_start,
                 2 * const.CELL_SIZE, 2 * const.CELL_SIZE)
            )

            self.screen.blit(production_image,
                             (x_start + const.CELL_SIZE - production_image.get_width() // 2,
                              y_start + const.CELL_SIZE - production_image.get_height() // 2))

            self.gui.draw_rect(  # inter-products
                self.screen, inter_products_color,
                (x_start + 3 * const.CELL_SIZE, y_start,
                 2 * const.CELL_SIZE, 2 * const.CELL_SIZE)
            )

            self.screen.blit(inter_products_image,
                             (x_start + 4 * const.CELL_SIZE - inter_products_image.get_width() // 2,
                              y_start + const.CELL_SIZE - inter_products_image.get_height() // 2))

            self.gui.draw_rect(  # logistics
                self.screen, logistics_color,
                (x_start + 6 * const.CELL_SIZE, y_start,
                 2 * const.CELL_SIZE, 2 * const.CELL_SIZE)
            )

            self.screen.blit(logistics_image,
                             (x_start + 7 * const.CELL_SIZE - logistics_image.get_width() // 2,
                              y_start + const.CELL_SIZE - logistics_image.get_height() // 2))

            # End of Bag

            for event in self.gui.get_events():
                if self.gui.get_event_type(event) == "QUIT":
                    self.quit()

                if 'ESCAPE' in self.gui.get_keystate():
                    self.show_bag_playing = False

                if self.gui.get_event_type(event) == 'MOUSEBUTTONDOWN' and event.button == 1:
                    # Переключение вкладок
                    if y_start + 2 * const.CELL_SIZE > event.pos[1] > y_start:
                        if x_start < event.pos[0] < x_start + 2 * const.CELL_SIZE:
                            self.module_playing = 'production'
                        elif x_start + 3 * const.CELL_SIZE < event.pos[0] < x_start + 5 * const.CELL_SIZE:
                            self.module_playing = 'inter-products'
                        elif x_start + 6 * const.CELL_SIZE < event.pos[0] < x_start + 8 * const.CELL_SIZE:
                            self.module_playing = 'logistics'

            self.gui.update_display()
            self.gui.tick_fps(self.clock, const.FPS)

    def draw_icon(self, color, x, y, width, height, img):
        self.gui.draw_rect(
            self.screen, color,
            (x, y, width, height)
        )
        img.set_colorkey(const.BLACK)
        self.screen.blit(img,
                         (x + (const.CELL_SIZE - img.get_width()) // 2,
                          y + (const.CELL_SIZE - img.get_height()) // 2))

    def show_start_screen(self):

        while self.start_screen_playing:
            background_image = self.gui.get_image('welcome_screen/screen_1/background_1.xcf')
            self.screen.blit(background_image, (0, 0))

            start_image = self.gui.get_image('welcome_screen/screen_1/start_button.xcf')
            credits_image = self.gui.get_image('welcome_screen/screen_1/credits_button.xcf')
            close_image = self.gui.get_image('welcome_screen/screen_1/close_button.xcf')

            self.screen.blit(start_image, (const.DISPLAY_W // 2 - 265 / 2, const.DISPLAY_H // 2))
            self.screen.blit(credits_image, (const.DISPLAY_W // 2 - 265 / 2, const.DISPLAY_H // 2 + 100))
            self.screen.blit(close_image, (const.DISPLAY_W // 2 - 265 / 2, const.DISPLAY_H // 2 + 200))

            mouse = self.gui.get_mouse_pos()
            if const.DISPLAY_W // 2 + 265 / 2 > mouse[0] > const.DISPLAY_W // 2 - 265 / 2:
                for event in self.gui.get_events():
                    if self.gui.get_event_type(event) == "MOUSEBUTTONDOWN":
                        if const.DISPLAY_H // 2 + 82 > mouse[1] > const.DISPLAY_H // 2:
                            self.start_screen_playing = False
                        elif const.DISPLAY_H // 2 + 182 > mouse[1] > const.DISPLAY_H // 2 + 100:
                            pass
                        elif const.DISPLAY_H // 2 + 282 > mouse[1] > const.DISPLAY_H // 2 + 200:
                            self.quit()

            self.events()

            self.gui.update_display()
            self.gui.tick_fps(self.clock, const.FPS)

    def choose_player_screen(self):

        while self.choose_player_screen_playing:
            background_image = self.gui.get_image('welcome_screen/screen_2/background_2.xcf')
            self.screen.blit(background_image, (0, 0))

            builder_image = self.gui.get_image('welcome_screen/screen_2/builder_button.xcf')
            usual_image = self.gui.get_image('welcome_screen/screen_2/usual_button.xcf')
            warrior_image = self.gui.get_image('welcome_screen/screen_2/warrior_button.xcf')

            self.screen.blit(builder_image, (const.DISPLAY_W // 2 - 265 / 2, const.DISPLAY_H // 2))
            self.screen.blit(usual_image, (const.DISPLAY_W // 2 - 265 / 2, const.DISPLAY_H // 2 + 100))
            self.screen.blit(warrior_image, (const.DISPLAY_W // 2 - 265 / 2, const.DISPLAY_H // 2 + 200))

            mouse = self.gui.get_mouse_pos()
            if const.DISPLAY_W // 2 + 265 / 2 > mouse[0] > const.DISPLAY_W // 2 - 265 / 2:
                for event in self.gui.get_events():
                    if self.gui.get_event_type(event) == "MOUSEBUTTONDOWN":
                        if const.DISPLAY_H // 2 + 82 > mouse[1] > const.DISPLAY_H // 2:
                            self.player_perk = 'big_bag'
                            self.choose_player_screen_playing = False
                        elif const.DISPLAY_H // 2 + 182 > mouse[1] > const.DISPLAY_H // 2 + 100:
                            self.player_perk = 'balanced'
                            self.choose_player_screen_playing = False
                        elif const.DISPLAY_H // 2 + 282 > mouse[1] > const.DISPLAY_H // 2 + 200:
                            self.player_perk = 'fast'
                            self.choose_player_screen_playing = False

            self.events()

            self.gui.update_display()
            self.gui.tick_fps(self.clock, const.FPS)

    def choose_map_screen(self):

        while self.choose_map_playing:
            background_image = self.gui.get_image('welcome_screen/screen_3/background_3.xcf')
            self.screen.blit(background_image, (0, 0))

            normal_image = self.gui.get_image('welcome_screen/screen_3/normal_button.xcf')
            hard_image = self.gui.get_image('welcome_screen/screen_3/hard_button.xcf')

            self.screen.blit(normal_image, (const.DISPLAY_W // 2 - 265 / 2, const.DISPLAY_H // 2))
            self.screen.blit(hard_image, (const.DISPLAY_W // 2 - 265 / 2, const.DISPLAY_H // 2 + 150))

            mouse = self.gui.get_mouse_pos()
            if const.DISPLAY_W // 2 + 265 / 2 > mouse[0] > const.DISPLAY_W // 2 - 265 / 2:
                for event in self.gui.get_events():
                    if self.gui.get_event_type(event) == "MOUSEBUTTONDOWN":
                        if const.DISPLAY_H // 2 + 82 > mouse[1] > const.DISPLAY_H // 2:
                            # creator = EasyMapCreator()
                            # self.map = creator.gen_map()
                            self.map = EasyMap()
                            with open('map.json', 'r+') as f:
                                self.map.load(json.load(f))
                            self.map_matr = self.map.get_map_matrix()
                            self.map_obj = self.map.get_map_objects()
                            self.choose_map_playing = False
                        elif const.DISPLAY_H // 2 + 232 > mouse[1] > const.DISPLAY_H // 2 + 150:
                            # creator = HardMapCreator()
                            # self.map = creator.gen_map()
                            self.map = HardMap()
                            with open('map.json', 'r+') as f:
                                self.map.load(json.load(f))
                            self.map_matr = self.map.get_map_matrix()
                            self.map_obj = self.map.get_map_objects()
                            self.choose_map_playing = False

            self.events()

            self.gui.update_display()
            self.gui.tick_fps(self.clock, const.FPS)

    def show_go_screen(self):
        pass
