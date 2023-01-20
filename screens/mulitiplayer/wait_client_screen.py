import socket
import threading

from main import MainWindow
from screens.abstract_screen import Screen
from screens.change_screen import change_screen
from screens.mulitiplayer.multiplayer_level_select_screen import MultiplayerLevelSelectScreen
from ui.text import draw_text


def server(ip, port):
    sock = socket.socket()
    sock.bind((ip, port))
    sock.listen(2)
    conn1, addr1 = sock.accept()

    conn2, addr2 = sock.accept()

    while True:
        data = conn1.recv(1024)
        if not data:
            continue
        conn2.send(data)

        data = conn2.recv(1024)
        if not data:
            continue
        conn1.send(data)


class WaitClientScreen(Screen):
    def __init__(self, game: MainWindow):
        super().__init__(game)

    def start(self):
        self.thread = threading.Thread(target=server, daemon=True, args=(self.game.ip, self.game.port))
        self.thread.start()

        self.sock = socket.socket()
        self.sock.connect(('localhost', self.game.port))

        draw_text(self.layers["gui"][0], (0, 20), "Ожидание подключения", 30, "white", centered=True)

    def update(self):
        self.sock.send("ready".encode())
        if self.sock.recv(1024).decode() == "ready":
            change_screen(self.game, MultiplayerLevelSelectScreen(self.game, self.thread, self.sock))

    def event(self, event):
        pass
