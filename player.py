import numpy as np
import pygame

from grid import BoxCollider
from main_window import FPS
from utilities import load_image
from vector import Vector


class Player(pygame.sprite.Sprite):
    image = load_image("player.png")
    g = 2000
    walk_speed = 0
    mass = 100

    def __init__(self, group: pygame.sprite.Group, grid):
        super().__init__(group)
        self.image = Player.image
        self.rect = self.image.get_rect()
        self.falling_speed = 0
        self.move_direction = 1
        self.grid = grid

        self.position = [100, 100]

        self.on_ground = False

        self.velocities = {}
        self.forces = {"g": Vector(0, self.mass * self.g)}

        self.ground_checker = BoxCollider(self.position[0], self.position[1] + 1, self.rect.width, 1)
        group.add(self.ground_checker)

        self.add_velocity(1, Vector(200, 0))
        self.add_velocity(2, Vector(0, -200))

    def add_velocity(self, key, velocity: Vector):
        self.velocities[key] = velocity

    def add_force(self, key, force):
        self.forces[key] = force

    def update(self):
        self.move()

        self.rect.x, self.rect.y = self.position

        self.ground_checker.rect.y = self.rect.y + self.rect.height
        self.ground_checker.rect.x = self.rect.x

        collider = self.grid.get_collider()
        self.on_ground = bool(pygame.sprite.collide_mask(self.ground_checker, collider))
        print(self.on_ground, self.forces, self.velocities)
        if self.on_ground:
            self.forces["g"] = Vector(0, 0)
            self.velocities["g"] = Vector(0, 0)
        else:
            self.forces["g"] = Vector(0, self.mass * self.g)
        # else:
        #     self.position[1] += self.falling_speed / FPS
        #     self.falling_speed += self.g / FPS
        #
        # while pygame.sprite.collide_mask(self, collider):
        #     self.position[1] -= 1
        #     self.ground_checker.rect.y -= 1
        #     self.rect.y = int(self.position[1])

    def move(self):
        for i in self.forces.keys():
            self.velocities[i] = self.velocities.get(i, Vector(0, 0)) + self.forces[i] / self.mass / FPS
        self.position = self.position + sum(self.velocities.values()) / FPS
