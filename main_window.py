from configparser import ConfigParser

import pygame

from game import Window
from icecream import install


from utilities import load_image, tile_texture

SIZE = 960, 540
FPS = 120


def show_fps(screen, fps):
    # font = pygame.font.Font(None, 20)
    # text = font.render(str(round(fps, 1)), True, (100, 255, 100))
    #
    # screen.blit(text, (0, 0))
    pygame.display.set_caption(str(fps))
    # print(fps)
    # print(fps)


class MainWindow(Window):
    def __init__(self, title, size):
        super().__init__(title, size)

    def start(self):
        background = load_image("background.png")
        multiple = max(self.surface.get_width() / background.get_width(), self.surface.get_height() / background.get_height())
        self.background = pygame.transform.scale(background, (background.get_width() * multiple, background.get_height() * multiple))

        self.config = ConfigParser()
        self.config.read("options.ini")

        from music import MusicManager
        self.music_manager = MusicManager(self, "data\\music")

    def update(self):
        pos = (self.surface.get_width() - self.background.get_width()) // 2, (self.surface.get_height() - self.background.get_height()) // 2
        self.surface.blit(self.background, pos)
        self.fps = self.clock.get_fps()
        if self.fps == 0:
            self.fps = 60
        show_fps(self.surface, self.clock.get_fps())

    def event(self, events: list[pygame.event.Event]):
        for event in events:
            if event.type == self.music_manager.MUSIC_END:
                self.music_manager.load_music()

    def close(self):
        with open("options.ini", "w") as config_file:
            self.config.write(config_file)


if __name__ == "__main__":
    install()
    main = MainWindow("123", SIZE)
