import pygame

from characters.abstract_characters import StaticCharacter


class Camera:
    def __init__(self):
        self.delta = (0, 0)

    def set_delta(self, x: int, y: int) -> None:
        self.delta = x, y

    def apply(self, sprite: pygame.sprite.Sprite):
        sprite.rect.x += self.delta[0]
        sprite.rect.y += self.delta[1]

        if isinstance(sprite, StaticCharacter):
            sprite.position[0] += self.delta[0]
            sprite.position[1] += self.delta[1]

