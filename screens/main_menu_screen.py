from main_window import MainWindow
from screens.abstract_screen import Screen
from screens.change_screen import change_screen
from screens.level_select_screen import LevelSelectScreen
from ui.button import Button


class MainMenuScreen(Screen):
    def __init__(self, game: MainWindow):
        super().__init__(game)


    def start(self):
        self.play = Button(self, "button.png", (0, 0), change_screen, size=(50, 20), text="Play",
                           hover_texture="hover.png", args=[LevelSelectScreen(self.game)])
        self.settings = Button(self, "button.png", (100, 100), lambda x: print(2), size=(50, 20), text="Settings",
                               hover_texture="hover.png")

    def update(self):
        self.game.surface.fill((0, 0, 0))
        self.all_sprites.draw(self.game.surface)
        self.buttons_group.update()

    def event(self, event):
        pass
