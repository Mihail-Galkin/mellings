import numpy as np
import pygame

from grid import BoxCollider, Dirt
from main_window import FPS
from utilities import load_image
from vector import Vector


def change_player_type(old, new):
    pass


class Player(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("player.png"), (17, 34))
    g = 2000
    walk_speed = 300
    mass = 100
    jump_height = 5

    def __init__(self, group: pygame.sprite.Group, grid):
        super().__init__(group)
        self.image = Player.image
        self.rect = self.image.get_rect()
        self.falling_speed = 0
        self.move_direction = 1
        self.grid = grid

        self.position = [200, 200]

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

        self.on_ground = bool(pygame.sprite.collide_mask(self.ground_checker, self.grid.get_collider()))
        self.ground_check()
        self.collision_check()
        self.custom()

    def ground_check(self):
        self.ground_checker.rect.y = self.rect.y + self.rect.height
        self.ground_checker.rect.x = self.rect.x

    def move(self):
        for i in self.forces.keys():
            self.velocities[i] = self.velocities.get(i, Vector(0, 0)) + self.forces[i] / self.mass / FPS
        self.position = self.position + sum(self.velocities.values()) / FPS

    def custom(self):
        pass

    def collision_check(self):
        collider = self.grid.get_collider()

        if self.on_ground:
            for i in self.forces:
                self.forces[i] = Vector(0, 0)
            for i in self.velocities:
                self.velocities[i] = Vector(0, 0)
            self.velocities["walk"] = Vector(self.move_direction * self.walk_speed, 0)
        else:
            self.velocities["walk"] = Vector(0, 0)
            self.forces["g"] = Vector(0, self.mass * self.g)
        delta = 0
        while pygame.sprite.collide_mask(self, collider) and delta < self.jump_height * self.grid.cell_size:
            delta += 1
            self.position[1] -= 1
            self.ground_checker.rect.y -= 1
            self.rect.y = int(self.position[1])
        if delta >= self.jump_height * self.grid.cell_size:
            self.position[1] += delta
            self.ground_checker.rect.y += delta
            self.rect.y = int(self.position[1])

            collide_position = pygame.sprite.collide_mask(self, collider)
            if collide_position[0] < self.rect.width // 2:
                self.move_direction = 1
            if collide_position[0] > self.rect.width // 2:
                self.move_direction = -1


class Blocker(Player):
    def __init__(self, *args, **kwargs):
        super(Blocker, self).__init__(*args, **kwargs)

    def collision_check(self):
        if not self.on_ground:
            change_player_type(self, Player)

        # TODO: Добавить коллизию


class Climber(Player):
    def __init__(self, *args, **kwargs):
        super(Climber, self).__init__(*args, **kwargs)


class Digger(Player):
    def __init__(self, *args, **kwargs):
        super(Digger, self).__init__(*args, **kwargs)
        self.b = True

    def custom(self):
        if self.on_ground and self.b:
            print(1231)
            pos = self.grid.to_local_coordinates(self.position)
            for i in range(-20, 20):
                for j in range(-20, 20):
                    self.grid.set_item(int(pos[0] + i), int(pos[1] + j), Dirt(self.grid, (int(pos[0] + i), int(pos[1] + j))))
            self.b = False

