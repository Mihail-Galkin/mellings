import pygame

from game import Window
from icecream import install

SIZE = 1920, 1080
FPS = 60


def show_fps(screen, fps):
    font = pygame.font.Font(None, 20)
    text = font.render(str(round(fps, 1)), True, (100, 255, 100))

    screen.blit(text, (0, 0))


class MainWindow(Window):
    def __init__(self, title, size):
        super().__init__(title, size)

    def start(self):
        pass

    def update(self):
        self.fps = self.clock.get_fps()
        if self.fps == 0:
            self.fps = 60
        show_fps(self.surface, self.clock.get_fps())

    def event(self, event):
        pass


if __name__ == "__main__":
    install()
    main = MainWindow("123", SIZE)
