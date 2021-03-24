from abc import ABC, abstractmethod


class GUI(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def set_caption(self, caption):
        pass

    @abstractmethod
    def set_screen(self, width, height):
        pass

    @abstractmethod
    def fill_screen(self, screen, color):
        pass

    @abstractmethod
    def set_clock(self):
        pass

    @abstractmethod
    def set_fps(self, clock, fps):
        pass

    @abstractmethod
    def group_sprites(self):
        pass

    @abstractmethod
    def add_sprite(self, group, sprite):
        pass

    @abstractmethod
    def update_sprites(self, group):
        pass

    @abstractmethod
    def draw_group(self, group, screen):
        pass

    @abstractmethod
    def get_surface(self, width, height):
        pass

    @abstractmethod
    def get_keystate(self):
        pass

    @abstractmethod
    def get_image(self, image):
        pass

    @abstractmethod
    def get_events(self):
        pass

    @abstractmethod
    def get_event_type(self, event):
        pass

    @abstractmethod
    def flip_display(self):
        pass

    @abstractmethod
    def quit_game(self):
        pass
