import socket

from level import load_level
from main import MainWindow
from screens.abstract_screen import Screen
from screens.change_screen import change_screen
from screens.mulitiplayer.multiplayer_game_screen import MultiplayerGameScreen
from ui.text import draw_text


class WaitHostScreen(Screen):
    def __init__(self, game: MainWindow):
        super().__init__(game)

    def start(self):
        self.sock = socket.socket()
        self.sock.connect((self.game.ip, self.game.port))

        draw_text(self.layers["gui"][0], (0, 20), "Ожидание хоста", 30, "white", centered=True)

    def update(self):
        self.sock.send("ready".encode())
        s = self.sock.recv(1024).decode()
        if s.startswith("level"):
            level = load_level("level", s.split()[1])
            change_screen(self.game, MultiplayerGameScreen(self.game, level, self.sock))

    def event(self, event):
        pass
