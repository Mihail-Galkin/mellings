from configparser import ConfigParser

import pygame

from game import Window
from icecream import install

from utilities import load_image


def show_fps(screen, fps):
    pygame.display.set_caption(f"Mellings (fps: {round(fps)})")


class MainWindow(Window):
    """
    Главный класс игры, унаследованный от Window.
    Класс переопределяет методы start, update, event, вызываемые Window

    """
    def __init__(self, title, size):
        super().__init__(title, size)

    def start(self):
        # Создание фона игры и увеличение до размером окна
        background = load_image("background.png")
        multiple = max(self.surface.get_width() / background.get_width(),
                       self.surface.get_height() / background.get_height())
        self.background = pygame.transform.scale(background, (background.get_width() * multiple,
                                                              background.get_height() * multiple))

        # Настройки игры сохраняются в файл
        self.config = ConfigParser()
        self.config.read("options.ini")

        # Фоновая музыка реализуется классом MusicManager. Импорт находится здесь для избежания circular import
        from music import MusicManager
        self.music_manager = MusicManager(self, "data\\music")

    def update(self):
        # Размещение фона игры
        pos = (self.surface.get_width() - self.background.get_width()) // 2, (
                    self.surface.get_height() - self.background.get_height()) // 2
        self.surface.blit(self.background, pos)

        # Обновление текущего fps и отображение
        self.fps = self.clock.get_fps()
        if self.fps == 0:
            self.fps = 1
        show_fps(self.surface, self.clock.get_fps())

    def event(self, events: list[pygame.event.Event]):
        for event in events:
            # Добавление в очередь музыки, когда предыдущая заканчивается. Используется собственный MUSIC_END event
            if event.type == self.music_manager.MUSIC_END:
                self.music_manager.load_music()

    def close(self):
        # Сохранение настроек при заверщении работы программы
        with open("options.ini", "w") as config_file:
            self.config.write(config_file)


if __name__ == "__main__":
    install()
    main = MainWindow("123", (960, 540))
