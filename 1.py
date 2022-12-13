import os
import random
import sys

import pygame as pygame


class Player(pygame.sprite.Sprite):
    image = load_image("player.png")

    def __init__(self, group):
        super().__init__(group)
        self.image = Player.image
        self.rect = self.image.get_rect()

        self.falling_speed = 0
        self.g = 0

        self.move_direction = 0
        self.speed = 10

    def update(self, *args):
        pass
