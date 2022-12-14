import os
import random
import sys

import pygame as pygame

from main_window import FPS
from utilities import load_image


class Player(pygame.sprite.Sprite):
    image = load_image("player.png")
    g = 1000
    walk_speed = 0

    def __init__(self, group, grid):
        super().__init__(group)
        self.image = Player.image
        self.rect = self.image.get_rect()
        self.falling_speed = 0
        self.move_direction = 1  # 1 - право, -1 - лево
        self.grid = grid

        self.x = 10
        self.y = 10

        self.on_ground = False

    def update(self):
        self.rect.x = int(self.x)
        # self.rect.y = self.y
        self.rect = self.rect.move(0, -self.rect.y + int(self.y))

        collider = self.grid.get_collider()
        self.x += self.move_direction * (self.walk_speed / FPS)
        while pygame.sprite.collide_mask(self, collider):
            self.x -= self.move_direction

        self.y += self.falling_speed / FPS
        self.falling_speed += self.g / FPS

        while pygame.sprite.collide_mask(self, collider):
            self.y -= 1

