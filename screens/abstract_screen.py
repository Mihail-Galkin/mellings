from abc import ABC, abstractmethod

import pygame

from main import MainWindow


class Screen(ABC):
    def __init__(self, game: MainWindow):
        self.players_group = pygame.sprite.Group()
        self.gui_sprites = pygame.sprite.Group()
        self.blockers = pygame.sprite.Group()
        self.game_sprites = pygame.sprite.Group()
        self.melling_changers_group = pygame.sprite.Group()

        self.game = game

        self.layers = {"gui": (pygame.Surface(self.game.size, pygame.SRCALPHA, 32).convert_alpha(), (0, 0))}

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def event(self, event):
        pass

