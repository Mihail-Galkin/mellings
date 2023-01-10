import socket
import threading

import pygame

from main import MainWindow
from screens.abstract_screen import Screen
from screens.changescreen import change_screen
from screens.level_select_screen import LevelSelectScreen
from screens.options_screen import OptionsScreen
from ui.button import Button
from ui.text import draw_text


def server(ip, port):
    sock = socket.socket()
    sock.bind(('192.168.0.6', 9090))
    sock.listen(2)
    conn1, addr1 = sock.accept()
    print(conn1, addr1)

    conn2, addr2 = sock.accept()
    print(conn2, addr2)

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
        self.thread = threading.Thread(target=server, daemon=True, args=(1, 2))
        self.thread.start()

        self.sock = socket.socket()
        self.sock.connect(('192.168.0.6', 9090))

        draw_text(self.layers["gui"][0], (0, 20), "Ожидание подключения", 30, "white", centered=True)

    def update(self):
        self.sock.send("ready".encode())
        if self.sock.recv(1024).decode() == "ready":
            print("connected")

    def event(self, event):
        pass
