import math
import pygame

import utilities
from animation import Animation
from colliders import BoxCollider
from screens.abstract_screen import Screen

from utilities import load_image
from vector import Vector


class StaticCharacter(pygame.sprite.Sprite):
    current_animation = Animation(load_image("walk.png"), (9, 1))
    animations = (current_animation,)

    def __init__(self, screen: Screen, position: tuple[int, int] = (0, 0), size=1):
        super().__init__(screen.game_sprites, screen.players_group)

        self.current_animation.apply(self)
        self.animation_cooldown = 0.08
        self.animation_current_cooldown = 0

        self.rect = self.image.get_rect()

        for i in self.animations:
            i.scale((self.rect.width * size, self.rect.height * size))
        self.current_animation.apply(self)
        self.rect = self.image.get_rect()

        self.screen = screen
        self.game = screen.game

        self.position = list(position)

        self.on_ground = False

        self.ground_checker = BoxCollider(self.position[0], self.position[1] + 1, self.rect.width, 1)
        screen.all_sprites.add(self.ground_checker)
        screen.camera_movable.add(self.ground_checker)

        self.mask_surface = pygame.Surface((self.rect.width, self.rect.height))
        self.mask_surface.fill("black")
        self.mask = pygame.mask.from_surface(self.mask_surface)

    def update(self):
        self.rect.x, self.rect.y = self.position

        self.ground_check()
        self.custom_update()
        self.animation_update()

    def animation_update(self):
        self.animation_current_cooldown += 1 / self.game.fps
        if self.animation_current_cooldown >= self.animation_cooldown:
            self.animation_current_cooldown = 0

            self.current_animation.next_frame()
            self.current_animation.apply(self)

    def ground_check(self):
        self.ground_checker.rect.y = self.rect.y + self.rect.height
        self.ground_checker.rect.x = self.rect.x
        self.on_ground = self.screen.is_collide(self.ground_checker)

    def custom_update(self):
        raise NotImplementedError()

    def resize(self, new_scale, change_position=True):
        m = new_scale[0] / self.rect.width

        if change_position:
            self.rect.x = int(self.rect.x * m)
            self.rect.y = int(self.rect.y * m)
            self.position = [self.rect.x, self.rect.y]
        self.rect.width, self.rect.height = new_scale
        for i in self.animations:
            width, height = i.frames[0].get_width(), i.frames[0].get_height()

            i.scale((width * m, height * m))

        self.ground_checker.resize((new_scale[0], 1))
        self.mask_surface = pygame.transform.scale(self.mask_surface, new_scale)
        self.mask = pygame.mask.from_surface(self.mask_surface)

        self.rect.width, self.rect.height = new_scale


class MovableCharacter(StaticCharacter):
    walk_speed = 40
    mass = 100
    jump_height = 5
    max_fall_distance = 20

    def __init__(self, screen: Screen, position: tuple[int, int] = (0, 0), size=1):
        super().__init__(screen, position, size=size)
        self.g = self.screen.g
        self.max_fall_velocity = (2 * self.g * self.max_fall_distance) ** 0.5
        self.move_direction = 1
        self.velocities = {}
        self.forces = {"g": Vector(0, self.mass * self.g)}

        self.rect.x, self.rect.y = self.position

    def custom_update(self):
        raise NotImplementedError()

    def update(self):
        self.ground_check()
        self.custom_update()
        self.collision_check()

        self.animation_update()
        self.current_animation.flipped = (self.move_direction == -1)

    def move(self, delta: Vector):
        sign = math.copysign(1, delta.x)

        for i in range(abs(delta.x)):
            self.rect.x += sign
            if self.screen.is_collide(self):
                self.rect.x -= sign
                self.position[0] = self.rect.x
                self.wall_reaction(sign)
                break

        sign = math.copysign(1, delta.y)

        for i in range(abs(delta.y)):
            self.rect.y += sign
            if self.screen.is_collide(self):
                self.rect.y -= sign
                self.position[1] = self.rect.y
                break

        for _ in range(200):
            if not self.screen.is_collide(self):
                break
            self.rect.y -= 1
            self.position[1] -= 1

        rect = self.screen.layers["game"][0].get_rect()
        if not self.rect.colliderect(rect):
            self.kill()
            self.ground_checker.kill()
            self.screen.players.pop(self)

    def collision_check(self):
        if self.on_ground:
            if "g" in self.velocities.keys() and \
                    self.velocities["g"].y > self.max_fall_velocity * self.screen.size_multiplier:
                self.kill()
                self.ground_checker.kill()
                self.screen.players.pop(self)
            self.velocities["g"] = Vector(0, 0)
            self.forces["g"] = Vector(0, 0)
            self.velocities["walk"] = Vector(self.move_direction * self.walk_speed, 0)
        else:
            self.velocities["walk"] = Vector(0, 0)
            self.forces["g"] = Vector(0, self.mass * self.g)

        for i in self.forces.keys():
            self.velocities[i] = self.velocities.get(i, Vector(0, 0)) + self.forces[i] / self.mass / self.game.fps
        total = sum(self.velocities.values()) / self.game.fps

        self.position[0] += total.x * self.screen.size_multiplier
        self.position[1] += total.y * self.screen.size_multiplier

        delta = Vector(int(self.position[0] - self.rect.x), int(self.position[1] - self.rect.y))
        self.move(delta)

    def get_wall_height(self, direction):
        if direction == 1:
            wall_checker = (BoxCollider(self.rect.x + self.rect.width, self.rect.y, 1, self.rect.height),
                            BoxCollider(self.rect.x, self.rect.y, self.rect.width, self.rect.height))
        else:
            wall_checker = (BoxCollider(self.rect.x - 1, self.rect.y, 1, self.rect.height),
                            BoxCollider(self.rect.x, self.rect.y, self.rect.width, self.rect.height))
        self.screen.camera_movable.add(wall_checker)
        delta = 0

        while True:

            delta += 1
            wall_checker[0].rect.y -= 1
            wall_checker[1].rect.y -= 1
            if self.screen.is_collide(wall_checker[1]):
                delta = 10 ** 5
                break
            if not self.screen.is_collide(wall_checker[0]):
                break

        wall_checker[0].kill()
        wall_checker[1].kill()

        return delta

    def wall_reaction(self, direction):
        height = self.get_wall_height(direction)
        if height < self.jump_height * self.screen.grid.cell_size:
            self.position[1] -= height
            self.position[0] += direction

            self.rect.x, self.rect.y = self.position
        else:
            self.move_direction = -direction
