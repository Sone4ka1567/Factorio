from pygameGUI import PygameGUI
from player import *
from camera import *

gui = PygameGUI()

gui.start()
gui.set_caption('ENDustrial')

screen = gui.set_screen(DISPLAY_W, DISPLAY_H)
running = True
clock = gui.set_clock()

# load player and camera
all_sprites = gui.group_sprites()
player = Player(**player_perks['fast'])
# camera = Camera()  # мб дефолтные размеры по-другому ?
gui.add_sprite(all_sprites, player)

while running:
    gui.set_fps(clock, FPS)
    # ввод процесса (события)
    for event in gui.get_events():
        # проверка закрытия окна
        if gui.get_event_type(event) == 'QUIT':
            running = False

    # обновление спрайтов
    gui.update_sprites(all_sprites)
    # camera.update(player)

    # Рендеринг
    gui.fill_screen(screen, BLACK)
    gui.draw_group(all_sprites, screen)
    # После отрисовки всего, переворачиваем экран

    # for sprite in all_sprites:
    # screen.blit(sprite.image, camera.apply(sprite))  # TODO
    gui.flip_display()

gui.quit_game()
