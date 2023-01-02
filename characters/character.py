import pygame

from characters.abstract_characters import MovableCharacter, StaticCharacter
from grid import BoxCollider
from grid_item import Stairs, Dirt
from utilities import load_image
from vector import Vector


class Digger(MovableCharacter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.current_cooldown = 0
        self.cooldown = 3

        self.radius = 6

    def custom_update(self):
        self.velocities["walk"] = 0
        self.current_cooldown += 1 / self.game.fps
        if self.current_cooldown >= self.cooldown and self.on_ground:
            self.current_cooldown = 0
            pos = self.position[0] + self.rect.width // 2, self.position[1] + self.rect.height
            pos = self.screen.grid.to_local_coordinates(pos)
            for i in range(-self.radius, self.radius + 1):
                for j in range(-self.radius, self.radius + 1):
                    if i ** 2 + j ** 2 <= self.radius ** 2:
                        self.screen.grid.set_item(int(pos[0] + i), int(pos[1] + j), None)


class Floater(MovableCharacter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def custom_update(self):
        if self.on_ground:
            self.forces["umbrella"] = 0
            self.velocities["umbrella"] = 0
        elif "g" in self.velocities.keys():
            self.velocities["umbrella"] = -self.velocities["g"] + Vector(0, 20)


class Climber(MovableCharacter):
    climb_speed = 100

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_climbing = False
        self.wall_checker = None

    def custom_update(self):
        collider = self.screen.grid.get_collider()
        if self.on_ground:
            pass
        if self.is_climbing:
            self.velocities["g"] = Vector(0, 0)
            self.forces["g"] = Vector(0, 0)

            self.wall_checker.rect.y = self.rect.y

            if not pygame.sprite.collide_mask(self.wall_checker, collider):
                self.is_climbing = False
                self.rect.x, self.rect.y = self.wall_checker.rect.x, self.wall_checker.rect.y
                self.position = [self.rect.x, self.rect.y]
                self.wall_checker.kill()
                self.wall_checker = None
                self.velocities["climb"] = Vector(0, 0)

    def wall_reaction(self, direction):
        height = self.get_wall_height(direction)
        if height < self.jump_height * self.screen.grid.cell_size:
            self.position[1] -= height
            self.position[0] += direction

            self.rect.x, self.rect.y = self.position
        else:
            self.is_climbing = True
            self.add_velocity("climb", Vector(0, -self.climb_speed))
            if direction == 1:
                self.wall_checker = BoxCollider(self.rect.x + self.rect.width, self.rect.y, 1, self.rect.height)
            else:
                self.wall_checker = BoxCollider(self.rect.x - 1, self.rect.y, 1, self.rect.height)
            self.groups()[0].add(self.wall_checker)


class Basher(MovableCharacter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.time_left = 10

        self.radius = 8

    def custom_update(self):
        self.time_left -= 1 / self.game.fps
        if self.time_left >= 0 and self.on_ground:
            pos = self.position[0] + self.rect.width, self.position[1] + self.rect.height // 2
            pos = self.screen.grid.to_local_coordinates(pos)
            for i in range(-self.radius, self.radius + 1):
                for j in range(-self.radius, self.radius + 1):
                    if i ** 2 + j ** 2 <= self.radius ** 2:
                        self.screen.grid.set_item(int(pos[0] + i), int(pos[1] + j), None)
            self.screen.grid.update_render()


class Miner(MovableCharacter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.time_left = 10

        self.radius = 10

    def custom_update(self):
        self.time_left -= 1 / self.game.fps
        if self.time_left >= 0 and self.on_ground:
            pos = self.position[0] + self.rect.width, self.position[1] + self.rect.height // 3 * 2
            pos = self.screen.grid.to_local_coordinates(pos)
            for i in range(-self.radius, self.radius + 1):
                for j in range(-self.radius, self.radius + 1):
                    if i ** 2 + j ** 2 <= self.radius ** 2:
                        self.screen.grid.set_item(int(pos[0] + i), int(pos[1] + j), None)
            self.screen.grid.update_render()


class Bomber(MovableCharacter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.time_left = 5

        self.radius = 20

    def custom_update(self):
        self.time_left -= 1 / self.game.fps
        if self.time_left <= 0:
            pos = self.position[0] + self.rect.width // 2, self.position[1] + self.rect.height // 2
            pos = self.screen.grid.to_local_coordinates(pos)
            for i in range(-self.radius, self.radius + 1):
                for j in range(-self.radius, self.radius + 1):
                    if i ** 2 + j ** 2 <= self.radius ** 2:
                        self.screen.grid.set_item(int(pos[0] + i), int(pos[1] + j), None)
            self.screen.grid.update_render()
            self.kill()
            self.game.players_group.remove(self)
            self.game.players.remove(self)


class Builder(MovableCharacter):
    platform_size = 5
    walk_speed = 20

    def __init__(self, *args, **kwargs):
        super(Builder, self).__init__(*args, **kwargs)
        self.cooldown = 0
        self.cooldown_max = 1
        self.first_placed = False

    def custom_update(self):
        if not self.first_placed and self.on_ground:
            self.build(self.move_direction)
            self.first_placed = True

    def wall_reaction(self, direction):
        height = self.get_wall_height(direction)
        if height < self.jump_height * self.screen.grid.cell_size:
            self.position[1] -= height
            self.position[0] += direction

            self.rect.x, self.rect.y = self.position

            self.build(direction)
        else:
            self.move_direction = -direction

    def build(self, direction):
        pos = self.position[0] + self.rect.width // 2, self.position[1]
        pos = list(map(int, self.screen.grid.to_local_coordinates(pos)))

        for i in range(self.platform_size):
            new = pos[:]
            new[0] += i * int(direction)
            new[1] -= 1
            self.screen.grid.set_item(*new, Stairs(self.screen.grid, tuple(new)))

        self.screen.grid.update_render()
        self.screen.grid.update_collider()


# TODO: функция для удаления окружностей
# TODO: передача в set_item не экземпляра класса
# TODO: все еще разворачивается, заметно на большом
# TODO: typing
# TODO: каждый лемминг в своем файле
# TODO: зависимость скорости от фпс
# TODO: fill -rect

class Blocker(StaticCharacter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def custom_update(self):
        pass
