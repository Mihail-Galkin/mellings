import typing

import pygame

from characters import Floater, Climber
from level import load_level
from main_window import MainWindow
from screens.abstract_screen import Screen
from ui.button import Button


class GameScreen(Screen):
    def __init__(self, game: MainWindow, level_path: str):
        self.level_path = level_path
        super().__init__(game)

    def start(self):
        self.grid = load_level(self.level_path).grid
        self.grid.rendered = self.grid.render()

        self.players = [Climber(self, (100, 100))]

        self.colliders = []

        self.btn = Button(self, "button.png", (0, 0), lambda x: print(1), size=(50, 20), text="Exit",
                          hover_texture="hover.png")

    def update(self):
        self.game.surface.fill((0, 0, 0))
        self.grid.draw(self.game.surface)
        self.all_sprites.draw(self.game.surface)
        self.players_group.update()
        self.buttons_group.update()

    def event(self, event):
        pass
