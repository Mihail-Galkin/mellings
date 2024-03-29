import csv
import os

import pygame.event

from level import load_level
from main import MainWindow
from screens.abstract_screen import Screen
from screens.change_screen import change_screen
from screens.game_screen import GameScreen
from ui.button import Button
from ui.level_widget import LevelWidget
from ui.text import draw_text

LEVELS_FOLDER = "level"


class LevelSelectScreen(Screen):
    """
    Окно выбора уровня. Если уровни не помещаются на экран, используются стрелочки для перелистывания
    """

    def __init__(self, game: MainWindow):
        super().__init__(game)
        self.current_page = 0
        self.max_page = 0
        self.pages = []

        self.widgets_on_page = []

    def start(self):
        from screens.main_menu_screen import MainMenuScreen
        self.back = Button(self, "button.png", (20, 20), change_screen, size=(80, 30), text="Выйти",
                           hover_texture="hover.png", args=[self.game, MainMenuScreen(self.game)])
        levels = []
        with open(os.path.join(LEVELS_FOLDER, "levels.csv"), encoding="utf8") as csvfile:
            reader = list(csv.reader(csvfile, delimiter=',', quotechar='"'))[1:]
            for row in reader:
                levels.append(load_level(LEVELS_FOLDER, row[0], completed=bool(row[1] == "1")))

        levels.sort(key=lambda level: level.title)
        on_page = self.game.size[0] // 105
        self.pages = [levels[i:i + on_page] for i in range(0, len(levels), on_page)]  # двумерный массив с уровнями
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
                LevelWidget(self, self.pages[self.current_page][i], (100, 100), 5, text_size=20, color=(173, 216, 230),
                            completed=self.pages[self.current_page][i].completed))
            self.widgets_on_page[-1].rect.x = 105 * i + indent
            self.widgets_on_page[-1].rect.y = 100

    def update(self):
        self.layers["gui"] = (pygame.Surface(self.game.size, pygame.SRCALPHA, 32).convert_alpha(), (0, 0))

        self.gui_sprites.draw(self.layers["gui"][0])
        self.gui_sprites.update()

        draw_text(self.layers["gui"][0], (20, 20), "Выберите уровень", 30, "white", centered=True)

    def event(self, events: list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT and self.current_page >= 1:
                self.current_page -= 1
                self.update_page()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT and self.current_page < self.max_page - 1:
                self.current_page += 1
                self.update_page()

    def level_selected(self, level):
        change_screen(self.game, GameScreen(self.game, level))
