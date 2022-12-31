# module_name, package_name, ClassName, method_name, ExceptionName, function_name,
# GLOBAL_CONSTANT_NAME, global_var_name, instance_var_name, function_parameter_name, local_var_name
import math
from abc import ABC
from typing import Union
import pygame

import utilities
from grid import BoxCollider
from main_window import MainWindow
from screens.abstract_screen import Screen
from utilities import load_image
from vector import Vector


class StaticCharacter(pygame.sprite.Sprite):
    # animation_sheet = pygame.transform.scale(load_image("player.png"), (17, 34))

    def __init__(self, screen: Screen, position: tuple[int, int] = (0, 0)):
        super().__init__(screen.all_sprites)
        screen.players_group.add(self)

        self.animation = utilities.cut_sheet(self.animation_sheet, 9, 1)
        self.image = self.animation[0]
        self.current_frame = 0
        self.animation_cooldown = 5
        self.animation_current_cooldown = 0

        self.rect = self.image.get_rect()

        self.screen = screen
        self.game = screen.game

        self.position = list(position)

        self.on_ground = False

        self.ground_checker = BoxCollider(self.position[0], self.position[1] + 1, self.rect.width, 1)
        screen.all_sprites.add(self.ground_checker)

    def update(self):
        self.rect.x, self.rect.y = self.position

        self.ground_check()
        self.custom_update()
        self.animation_update()


    def animation_update(self):
        self.animation_current_cooldown += 1
        if self.animation_current_cooldown >= self.animation_cooldown:
            self.animation_current_cooldown = 0

            self.current_frame = (self.current_frame + 1) % len(self.animation)
            self.image = self.animation[self.current_frame]


    def ground_check(self):
        self.ground_checker.rect.y = self.rect.y + self.rect.height
        self.ground_checker.rect.x = self.rect.x

        self.on_ground = bool(pygame.sprite.collide_mask(self.ground_checker, self.screen.grid.get_collider()))

    def custom_update(self):
        raise NotImplementedError()


class MovableCharacter(StaticCharacter):
    animation_sheet = load_image("walk.png")
    g = 400
    walk_speed = 40
    mass = 100
    jump_height = 10

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

        self.animation_update()

    def add_velocity(self, key, velocity: Vector):
        self.velocities[key] = velocity

    def add_force(self, key, force):
        self.forces[key] = force

    def move(self, delta: Vector):
        collider = self.screen.grid.get_collider()

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
        collider = self.screen.grid.get_collider()
        if direction == 1:
            wall_checker = (BoxCollider(self.rect.x + self.rect.width - 1, self.rect.y, 0, self.rect.height),
                            BoxCollider(self.rect.x, self.rect.y, self.rect.width - 1, self.rect.height - 1))
        else:
            wall_checker = (BoxCollider(self.rect.x - 1, self.rect.y, 0, self.rect.height),
                            BoxCollider(self.rect.x, self.rect.y, self.rect.width - 1, self.rect.height - 1))

        delta = 0

        while True:
            delta += 1
            wall_checker[0].rect.y -= 1
            wall_checker[1].rect.y -= 1
            if pygame.sprite.collide_mask(wall_checker[1], collider):
                delta = 10 ** 5
                break
            if not pygame.sprite.collide_mask(wall_checker[0], collider):
                break

        wall_checker[0].kill()
        wall_checker[1].kill()

        return delta

    def wall_reaction(self, direction):
        height = self.get_wall_height(direction)
        ic(height)
        if height < self.jump_height * self.screen.grid.cell_size:
            self.position[1] -= height
            self.position[0] += direction

            self.rect.x, self.rect.y = self.position
        else:
            self.move_direction = -direction
