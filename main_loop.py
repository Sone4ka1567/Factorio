from game import Game
from pygamegui import PygameGUI


game = Game(PygameGUI())
game.show_start_screen()
game.choose_player_screen()
game.choose_map_screen()
game.new()
game.run()
game.show_go_screen()
