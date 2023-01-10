import pickle
import socket
import threading

import pygame

from main import MainWindow
from screens.abstract_screen import Screen
from screens.changescreen import change_screen
from screens.game_screen import GameScreen
from screens.level_select_screen import LevelSelectScreen
from screens.options_screen import OptionsScreen
from ui.button import Button
from ui.text import draw_text


class WaitHostScreen(Screen):
    def __init__(self, game: MainWindow):
        super().__init__(game)

    def start(self):
        self.sock = socket.socket()
        self.sock.connect(('192.168.0.6', 9090))

        draw_text(self.layers["gui"][0], (0, 20), "Ожидание хоста", 30, "white", centered=True)

    def update(self):
        self.sock.send("ready".encode())
        try:
            level = pickle.loads(self.sock.recv(1024))
            change_screen(self.game, GameScreen(self.game, level))
        except pickle.UnpicklingError:
            pass

    def event(self, event):
        pass
