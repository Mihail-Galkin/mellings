from abc import ABC, abstractmethod

import pygame

from main_window import MainWindow


class Screen(ABC):
    def __init__(self, game: MainWindow):
        self.players_group = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.buttons_group = pygame.sprite.Group()
        self.camera_movable = pygame.sprite.Group()

        self.game = game

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def event(self, event):
        pass
