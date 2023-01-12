import pygame

from main import MainWindow
from screens.abstract_screen import Screen
from screens.change_screen import change_screen

from ui.button import Button
from ui.text import draw_text


class EndScreen(Screen):
    def __init__(self, game: MainWindow, characters_completed, characters, characters_need):
        super().__init__(game)
        self.characters_completed = characters_completed
        self.characters = characters
        self.characters_need = characters_need

    def start(self):
        from screens.main_menu_screen import MainMenuScreen

        x_indent = (self.layers["gui"][0].get_width() - 100) // 2
        y_indent = self.layers["gui"][0].get_height() - 70
        self.return_btn = Button(self, "button.png", (x_indent, y_indent), change_screen,
                                 size=(100, 50), text="Меню",
                                 hover_texture="hover.png", args=[self.game, MainMenuScreen(self.game)])

    def update(self):
        self.layers["gui"] = (pygame.Surface(self.game.size, pygame.SRCALPHA, 32).convert_alpha(), (0, 0))

        self.gui_sprites.draw(self.layers["gui"][0])
        self.gui_sprites.update()

        draw_text(self.layers["gui"][0], (20, 20),
                  f"Уровень {'успешно' if self.characters_need <= self.characters_completed else 'не'} пройден",
                  30, "white", centered=True)
        draw_text(self.layers["gui"][0], (20, 50),
                  f"Прошло: {self.characters_completed} из {self.characters} ({round(self.characters_completed / self.characters * 100)}%)",
                  20, "white")

    def event(self, events):
        pass
