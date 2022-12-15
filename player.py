import numpy as np
import pygame

from grid import BoxCollider
from main_window import FPS
from utilities import load_image
from vector import Vector


class Player(pygame.sprite.Sprite):
    image = load_image("player.png")
    g = 500
    walk_speed = 0
    mass = 100

    def __init__(self, group: pygame.sprite.Group, grid):
        super().__init__(group)
        self.image = Player.image
        self.rect = self.image.get_rect()
        self.falling_speed = 0
        self.move_direction = 1
        self.grid = grid

        self.position = np.array([100, 100])

        self.on_ground = False

        self.velocity = Vector(0, 0)
        self.force = Vector(0, 0)

        self.ground_checker = BoxCollider(self.position[0], self.position[1] + 1, self.rect.width, 1)
        group.add(self.ground_checker)

        self.add_force(Vector(0, self.g * self.mass))
        self.add_velocity(Vector(200, 0))
        self.add_velocity(Vector(0, -200))

    def add_velocity(self, velocity: Vector):
        self.velocity = self.velocity + velocity

    def add_force(self, force):
        self.force = self.force + force

    def update(self):
        self.move()

        self.rect.x, self.rect.y = self.position



        # self.ground_checker.rect.y = self.rect.y + self.rect.height
        # self.ground_checker.rect.x = self.rect.x
        #
        # collider = self.grid.get_collider()
        # self.on_ground = bool(pygame.sprite.collide_mask(self.ground_checker, collider))
        #
        # if self.on_ground:
        #     self.falling_speed = 0
        # else:
        #     self.position[1] += self.falling_speed / FPS
        #     self.falling_speed += self.g / FPS
        #
        # while pygame.sprite.collide_mask(self, collider):
        #     self.position[1] -= 1
        #     self.ground_checker.rect.y -= 1
        #     self.rect.y = int(self.position[1])

    def move(self):
        self.velocity = self.velocity + self.force / self.mass / FPS
        self.position = self.position + np.array(list(self.velocity / FPS))
