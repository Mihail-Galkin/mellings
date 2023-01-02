from os import listdir
from os.path import isfile, join

import pygame.event

from level import load_level
from main_window import MainWindow
from screens.abstract_screen import Screen
from ui.level_widget import LevelWidget
from utilities import draw_text

LEVELS_FOLDER = "level"


class LevelSelectScreen(Screen):
    def __init__(self, game: MainWindow):
        super().__init__(game)
        self.current_page = 0
        self.max_page = 0
        self.pages = []

        self.widgets_on_page = []

    def start(self):
        files = [f.rsplit(".", maxsplit=1)[0] for f in listdir(LEVELS_FOLDER) if isfile(join(LEVELS_FOLDER, f))]
        files = list(set(files))
        levels = []
        for i in range(len(files)):
            levels.append(load_level(LEVELS_FOLDER, files[i]))
        levels.sort(key=lambda level: level.title)
        on_page = self.game.size[0] // 105
        self.pages = [levels[i:i + on_page] for i in range(0, len(levels), on_page)]
        self.max_page = len(self.pages)

        self.update_page()

    def update_page(self):
        for i in self.widgets_on_page:
            i.kill()
            del i
        on_page = len(self.pages[self.current_page])
        indent = (self.game.size[0] - on_page * 100 - (on_page - 1) * 5) // 2
        for i in range(len(self.pages[self.current_page])):
            self.widgets_on_page.append(
                LevelWidget(self, self.pages[self.current_page][i], (100, 100), 5, text_size=20))
            self.widgets_on_page[-1].rect.x = 105 * i + indent
            self.widgets_on_page[-1].rect.y = 100

    def update(self):
        self.all_sprites.draw(self.game.surface)
        self.all_sprites.update()

        draw_text(self.game.surface, (5, 5), "Выберите уровень:", 30, "white")

    def event(self, events: list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT and self.current_page >= 1:
                self.current_page -= 1
                self.update_page()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT and self.current_page < self.max_page - 1:
                self.current_page += 1
                self.update_page()
