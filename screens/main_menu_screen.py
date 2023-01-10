import sys

import pygame.event

from main import MainWindow
from screens.abstract_screen import Screen
from screens.changescreen import change_screen
from screens.level_select_screen import LevelSelectScreen
from screens.multiplayer_screen import MultiplayerScreen
from screens.options_screen import OptionsScreen
from ui.button import Button
from ui.text import draw_text


def close(game: MainWindow):
    game.close()
    sys.exit(0)


class MainMenuScreen(Screen):
    def __init__(self, game: MainWindow):
        super().__init__(game)

    def start(self):
        BUTTON_WIDTH = 130
        self.h_indent = (self.layers["gui"][0].get_width() - BUTTON_WIDTH * 4) // 5
        self.v_indent = self.layers["gui"][0].get_height() // 3
        self.play = Button(self, "button.png", (self.h_indent, self.v_indent * 2), change_screen,
                           size=(BUTTON_WIDTH, 50), text="Играть",
                           hover_texture="hover.png", args=[self.game, LevelSelectScreen(self.game)])
        self.multiplayer = Button(self, "button.png", (self.h_indent * 2 + BUTTON_WIDTH, self.v_indent * 2),
                                  change_screen,
                                  size=(BUTTON_WIDTH, 50), text="Сетевая игра",
                                  hover_texture="hover.png", args=[self.game, MultiplayerScreen(self.game)])
        self.settings = Button(self, "button.png", (self.h_indent * 3 + BUTTON_WIDTH * 2, self.v_indent * 2),
                               change_screen,
                               size=(BUTTON_WIDTH, 50), text="Настройки",
                               hover_texture="hover.png", args=[self.game, OptionsScreen(self.game)])
        self.quit = Button(self, "button.png", (self.h_indent * 4 + BUTTON_WIDTH * 3, self.v_indent * 2), close,
                           size=(BUTTON_WIDTH, 50), text="Выйти",
                           hover_texture="hover.png", args=[self.game])

    def update(self):
        self.layers["gui"] = (pygame.Surface(self.game.size, pygame.SRCALPHA, 32).convert_alpha(), (0, 0))

        self.gui_sprites.draw(self.layers["gui"][0])
        self.gui_sprites.update()

        draw_text(self.layers["gui"][0], (0, self.v_indent), "Mellings", 90, color="forestgreen", centered=True)

    def event(self, event):
        pass
