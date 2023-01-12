import pygame

from screens.abstract_screen import Screen
from screens.change_screen import change_screen

from ui.button import Button
from ui.text import draw_text


class WinnerScreen(Screen):
    def __init__(self, game, message):
        super().__init__(game)
        self.message = message

    def start(self):
        from screens.main_menu_screen import MainMenuScreen
        self.back = Button(self, "button.png", (20, 20), change_screen, size=(80, 30), text="Выйти",
                           hover_texture="hover.png", args=[self.game, MainMenuScreen(self.game)])

    def update(self):
        self.layers["gui"] = (pygame.Surface(self.game.size, pygame.SRCALPHA, 32).convert_alpha(), (0, 0))

        self.gui_sprites.draw(self.layers["gui"][0])
        self.gui_sprites.update()

        draw_text(self.layers["gui"][0], (20, 20), self.message, 25, "white", centered=True)

    def event(self, event):
        pass
