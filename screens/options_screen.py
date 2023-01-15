import pygame

from main import MainWindow

from screens.abstract_screen import Screen
from screens.change_screen import change_screen

from ui.button import Button
from ui.text import draw_text


class OptionsScreen(Screen):
    """
    Окно настройки. Реализовано изменение громкости фоновой музыки
    """
    def __init__(self, game: MainWindow):
        super().__init__(game)

    def start(self):
        from screens.main_menu_screen import MainMenuScreen
        indent = self.layers["gui"][0].get_height() // 2
        self.volume_down = Button(self, "button.png", (170, indent),
                                  self.game.music_manager.add_volume, (20, 20), text="-", args=[-0.05])
        self.volume_up = Button(self, "button.png", (250, indent),
                                self.game.music_manager.add_volume, (20, 20), text="+", args=[0.05])
        self.back = Button(self, "button.png", (20, 20), change_screen, size=(80, 30), text="Выйти",
                           hover_texture="hover.png", args=[self.game, MainMenuScreen(self.game)])

    def update(self):
        self.layers["gui"] = (pygame.Surface(self.game.size, pygame.SRCALPHA, 32).convert_alpha(), (0, 0))

        self.gui_sprites.draw(self.layers["gui"][0])
        self.gui_sprites.update()

        draw_text(self.layers["gui"][0], (0, 20), "Настройки", 30, "white", centered=True)
        indent = self.layers["gui"][0].get_height() // 2
        draw_text(self.layers["gui"][0], (20, indent), "Громкость:", 25, "white")
        draw_text(self.layers["gui"][0], (200, indent), f"{round(self.game.music_manager.current_volume * 100)}%", 25,
                  "white")

    def event(self, events):
        pass
