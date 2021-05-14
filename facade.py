from abc import ABC, abstractmethod


class GUI(ABC):

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def set_caption(self, caption):
        pass

    @abstractmethod
    def set_screen(self, width, height, hwsurf, double_buffer):
        pass

    @abstractmethod
    def set_music(self, file):
        pass

    @abstractmethod
    def stop_music(self):
        pass

    @abstractmethod
    def fill_screen(self, screen, color):
        pass

    @abstractmethod
    def set_clock(self):
        pass

    @abstractmethod
    def tick_fps(self, clock, fps):
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
    def get_display_info(self):
        pass

    @abstractmethod
    def get_events(self):
        pass

    @abstractmethod
    def get_mouse_pos(self):
        pass

    @abstractmethod
    def get_mouse_pressed(self):
        pass

    @abstractmethod
    def get_font(self, name, size):
        pass

    @abstractmethod
    def get_sys_font(self, name, size):
        pass

    @abstractmethod
    def get_rect(self, x_border, y_border, width, height):
        pass

    @abstractmethod
    def get_event_type(self, event):
        pass

    @abstractmethod
    def draw_line(self, screen, color, start, end):
        pass

    @abstractmethod
    def draw_rect(self, screen, color, coordinates):
        pass

    @abstractmethod
    def flip_display(self):
        pass

    @abstractmethod
    def update_display(self):
        pass

    @abstractmethod
    def get_hwsurface(self):
        pass

    @abstractmethod
    def get_double_buffer(self):
        pass

    @abstractmethod
    def quit_game(self):
        pass
