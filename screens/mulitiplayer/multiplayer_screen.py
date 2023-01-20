import pygame

from main import MainWindow
from screens.abstract_screen import Screen
from screens.change_screen import change_screen

from screens.mulitiplayer.wait_client_screen import WaitClientScreen
from screens.mulitiplayer.wait_host_screen import WaitHostScreen
from ui.button import Button
from ui.text import draw_text


class MultiplayerScreen(Screen):
    def __init__(self, game: MainWindow):
        super().__init__(game)

    def start(self):
        from screens.main_menu_screen import MainMenuScreen
        BUTTON_WIDTH = 130
        self.h_indent = (self.layers["gui"][0].get_width() - BUTTON_WIDTH * 2) // 3
        self.v_indent = self.layers["gui"][0].get_height() // 2
        self.play = Button(self, "button.png", (self.h_indent, self.v_indent), change_screen,
                           size=(BUTTON_WIDTH, 50), text="Создать",
                           hover_texture="hover.png", args=[self.game, WaitClientScreen(self.game)])
        self.settings = Button(self, "button.png", (self.h_indent * 2 + BUTTON_WIDTH, self.v_indent), change_screen,
                               size=(BUTTON_WIDTH, 50), text="Зайти",
                               hover_texture="hover.png", args=[self.game, WaitHostScreen(self.game)])
        self.back = Button(self, "button.png", (20, 20), change_screen, size=(80, 30), text="Выйти",
                           hover_texture="hover.png", args=[self.game, MainMenuScreen(self.game)])

    def update(self):
        self.layers["gui"] = (pygame.Surface(self.game.size, pygame.SRCALPHA, 32).convert_alpha(), (0, 0))
        self.gui_sprites.draw(self.layers["gui"][0])
        self.gui_sprites.update()

        draw_text(self.layers["gui"][0], (0, 20), "Сетевая игра", 30, "white", centered=True)

    def event(self, event):
        pass
