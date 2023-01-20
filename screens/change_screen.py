from main import MainWindow
from screens.abstract_screen import Screen


def change_screen(game: MainWindow, new_screen: Screen):
    game.screen = new_screen
    game.screen.start()
