from typing import Callable

import pygame

from main_window import MainWindow
from screens.abstract_screen import Screen
from ui.button import Button
from utilities import load_image


class LemmingButton(pygame.sprite.Sprite):
    def __init__(self, screen: Screen, texture: str, lemming_class: type,
                 position: tuple[int, int], listener: Callable[[MainWindow, int], None], arg=None):
        super().__init__(screen.all_sprites, screen.buttons_group)

        self.default_image = load_image(texture)
        self.activated_image = load_image(f"{texture[:-4]}_activated.jpg")

        self.activated = False
        self.clicked = False
        self.lemming_class = lemming_class

        self.image = self.default_image
        self.rect = self.image.get_rect()

        self.screen = screen
        self.rect.x, self.rect.y = position
        self.listener = listener
        self.arg = arg

    def set_activated(self, b):
        self.activated = b
        if b:
            self.image = self.activated_image
        else:
            self.image = self.default_image

    def update(self):
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False
        if self.rect.collidepoint(*pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and not self.clicked:
            self.listener(self.screen.game, self.arg)
            self.clicked = True
