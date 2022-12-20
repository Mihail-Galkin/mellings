# module_name, package_name, ClassName, method_name, ExceptionName, function_name,
# GLOBAL_CONSTANT_NAME, global_var_name, instance_var_name, function_parameter_name, local_var_name
import math
from abc import ABC
from typing import Union

import pygame

from grid import BoxCollider
from main_window import MainWindow
from utilities import load_image
from vector import Vector


class StaticCharacter(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("player.png"), (17, 34))

    def __init__(self, group: pygame.sprite.Group, game: MainWindow, position: tuple[int, int] = (0, 0)):
        super().__init__(group)
        self.image = StaticCharacter.image
        self.rect = self.image.get_rect()

        self.game = game

        self.position = list(position)

        self.on_ground = False

        self.ground_checker = BoxCollider(self.position[0], self.position[1] + 1, self.rect.width, 1)
        group.add(self.ground_checker)

    def update(self):
        self.rect.x, self.rect.y = self.position

        self.ground_check()
        self.custom_update()

    def ground_check(self):
        self.ground_checker.rect.y = self.rect.y + self.rect.height
        self.ground_checker.rect.x = self.rect.x

        self.on_ground = bool(pygame.sprite.collide_mask(self.ground_checker, self.game.grid.get_collider()))

    def custom_update(self):
        raise NotImplementedError()


class MovableCharacter(StaticCharacter):
    g = 200
    walk_speed = 100
    mass = 100
    jump_height = 5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.move_direction = 1
        self.velocities = {}
        self.forces = {"g": Vector(0, self.mass * self.g)}

        self.rect.x, self.rect.y = self.position

        # self.add_velocity(1, Vector(100, 0))
        # self.add_velocity(2, Vector(0, -100))

    def custom_update(self):
        # raise NotImplementedError()
        pass

    def update(self):
        self.ground_check()
        self.custom_update()
        self.collision_check()

    def add_velocity(self, key, velocity: Vector):
        self.velocities[key] = velocity

    def add_force(self, key, force):
        self.forces[key] = force

    def move(self, delta: Vector):
        collider = self.game.grid.get_collider()

        sign = -math.copysign(1, delta.x)

        for i in range(abs(delta.x)):
            self.rect.x += sign
            if pygame.sprite.collide_mask(self, collider):
                self.rect.x -= sign
                self.position[0] = self.rect.x

                self.wall_reaction(sign)
                break

        sign = -math.copysign(1, delta.y)

        for i in range(abs(delta.y)):
            self.rect.y += sign
            if pygame.sprite.collide_mask(self, collider):
                self.rect.y -= sign
                self.position[1] = self.rect.y
                break

    def collision_check(self):
        if self.on_ground:
            self.velocities["g"] = Vector(0, 0)
            self.forces["g"] = Vector(0, 0)
            self.velocities["walk"] = Vector(self.move_direction * self.walk_speed, 0)
        else:
            self.velocities["walk"] = Vector(0, 0)
            self.forces["g"] = Vector(0, self.mass * self.g)

        for i in self.forces.keys():
            self.velocities[i] = self.velocities.get(i, Vector(0, 0)) + self.forces[i] / self.mass / self.game.fps
        total = sum(self.velocities.values()) / self.game.fps

        self.position[0] += total.x
        self.position[1] += total.y

        delta = Vector(int(self.rect.x - self.position[0]), int(self.rect.y - self.position[1]))
        self.move(delta)

    def get_wall_height(self, direction):
        collider = self.game.grid.get_collider()
        if direction == 1:
            wall_checker = (BoxCollider(self.rect.x + self.rect.width - 1, self.rect.y, 1, self.rect.height),
                            BoxCollider(self.rect.x + self.rect.width, self.rect.y, 1, self.rect.height))
        else:
            wall_checker = (BoxCollider(self.rect.x, self.rect.y, 1, self.rect.height),
                            BoxCollider(self.rect.x - 1, self.rect.y, 1, self.rect.height))

        self.groups()[0].add(wall_checker)

        delta = 0

        while True:
            delta += 1
            wall_checker[0].rect.y -= 1
            wall_checker[1].rect.y -= 1
            if pygame.sprite.collide_mask(wall_checker[0], collider):
                delta = 10 ** 5
                break
            if not pygame.sprite.collide_mask(wall_checker[1], collider):
                break

        wall_checker[0].kill()
        wall_checker[1].kill()

        return delta

    def wall_reaction(self, direction):
        height = self.get_wall_height(direction)
        if height < self.jump_height * self.game.grid.cell_size:
            self.position[1] -= height
            self.position[0] += direction

            self.rect.x, self.rect.y = self.position
        else:
            self.move_direction = -direction
