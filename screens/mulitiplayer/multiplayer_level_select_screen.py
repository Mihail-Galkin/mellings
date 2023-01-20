import socket

from screens.change_screen import change_screen
from screens.level_select_screen import LevelSelectScreen
from screens.mulitiplayer.multiplayer_game_screen import MultiplayerGameScreen


class MultiplayerLevelSelectScreen(LevelSelectScreen):
    def __init__(self, game, thread, sock: socket.socket):
        super().__init__(game)
        self.thread = thread
        self.sock = sock

    def level_selected(self, level):
        change_screen(self.game, MultiplayerGameScreen(self.game, level, self.sock, thread=self.thread))
        self.sock.send(("level " + level.filename).encode())
