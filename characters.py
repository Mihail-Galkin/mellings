import pygame

from abstract_characters import MovableCharacter, StaticCharacter
from grid import BoxCollider
from grid_item import Stairs
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
            pos = self.game.grid.to_local_coordinates(pos)
            for i in range(-self.radius, self.radius + 1):
                for j in range(-self.radius, self.radius + 1):
                    if i ** 2 + j ** 2 <= self.radius ** 2:
                        self.game.grid.set_item(int(pos[0] + i), int(pos[1] + j), None)
            self.game.grid.rendered = self.game.grid.render()


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
        collider = self.game.grid.get_collider()
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
        if height < self.jump_height * self.game.grid.cell_size:
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
            pos = self.game.grid.to_local_coordinates(pos)
            for i in range(-self.radius, self.radius + 1):
                for j in range(-self.radius, self.radius + 1):
                    if i ** 2 + j ** 2 <= self.radius ** 2:
                        self.game.grid.set_item(int(pos[0] + i), int(pos[1] + j), None)
            self.game.grid.rendered = self.game.grid.render()


class Miner(MovableCharacter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.time_left = 10

        self.radius = 10

    def custom_update(self):
        self.time_left -= 1 / self.game.fps
        if self.time_left >= 0 and self.on_ground:
            pos = self.position[0] + self.rect.width, self.position[1] + self.rect.height // 3 * 2
            pos = self.game.grid.to_local_coordinates(pos)
            for i in range(-self.radius, self.radius + 1):
                for j in range(-self.radius, self.radius + 1):
                    if i ** 2 + j ** 2 <= self.radius ** 2:
                        self.game.grid.set_item(int(pos[0] + i), int(pos[1] + j), None)
            self.game.grid.rendered = self.game.grid.render()


class Bomber(MovableCharacter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.time_left = 5

        self.radius = 20

    def custom_update(self):
        self.time_left -= 1 / self.game.fps
        if self.time_left <= 0:
            pos = self.position[0] + self.rect.width // 2, self.position[1] + self.rect.height // 2
            pos = self.game.grid.to_local_coordinates(pos)
            for i in range(-self.radius, self.radius + 1):
                for j in range(-self.radius, self.radius + 1):
                    if i ** 2 + j ** 2 <= self.radius ** 2:
                        self.game.grid.set_item(int(pos[0] + i), int(pos[1] + j), None)
            self.game.grid.rendered = self.game.grid.render()
            self.kill()
            self.game.players_group.remove(self)
            self.game.players.remove(self)


class Builder(MovableCharacter):
    platform_size = 1

    def __init__(self, *args, **kwargs):
        super(Builder, self).__init__(*args, **kwargs)
        self.cooldown = 0
        self.cooldown_max = 1

    def custom_update(self):
        if self.on_ground:
            self.cooldown = 0
            pos = self.position[0] + self.rect.width // 2, self.position[1] + self.rect.height
            pos = list(map(int, self.game.grid.to_local_coordinates(pos)))

            for i in range(self.platform_size):
                pos[0] += i
                pos[1] -= 1
                self.game.grid.set_item(*pos, Stairs(self.game.grid, tuple(pos)))
            self.game.grid.rendered = self.game.grid.render()

# TODO: функция для удаления окружностей
# TODO: передача в set_item не экземпляра класса


class Blocker(StaticCharacter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def custom_update(self):
        pass
