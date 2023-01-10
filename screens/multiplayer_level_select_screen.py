import pickle
import socket

from screens.changescreen import change_screen
from screens.game_screen import GameScreen
from screens.level_select_screen import LevelSelectScreen


class MultiplayerLevelSelectScreen(LevelSelectScreen):
    def __init__(self, game, thread, sock: socket.socket):
        super().__init__(game)
        self.thread = thread
        self.sock = sock

    def level_selected(self, level):
        change_screen(self.game, GameScreen(self.game, level))
        self.sock.send(pickle.dumps(level))