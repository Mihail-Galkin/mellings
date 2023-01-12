import random

import pygame

from screens.game_screen import GameScreen


class Particle(pygame.sprite.Sprite):
    """
    Класс создает спрайт случайного размера и обрабатывает его физику
    """
    def __init__(self, screen: GameScreen, sprite: pygame.Surface, pos: tuple[int, int], dx: int, dy: int):
        super().__init__(screen.game_sprites)
        sprites = []
        for scale in (1, 2, 5):
            sprites.append(pygame.transform.scale(sprite, (scale, scale)))

        self.image = random.choice(sprites)
        self.rect = self.image.get_rect()

        self.screen = screen
        self.game = screen.game

        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos

        self.gravity = 100

        self.screen_rect = (0, 0, *self.game.size)

        self.pos = list(pos)

    def update(self) -> None:
        self.rect.x, self.rect.y = self.pos
        self.velocity[1] += self.gravity / self.game.fps

        self.pos[0] += self.velocity[0] / self.game.fps
        self.pos[1] += self.velocity[1] / self.game.fps
        if not self.rect.colliderect(self.screen_rect):
            self.kill()


def create_particles(screen: GameScreen, sprite: pygame.Surface,
                     position: tuple[int, int], particle_count: int = 20) -> None:
    numbers = list(range(-100, 101))
    numbers.remove(0)
    for _ in range(particle_count):
        Particle(screen, sprite, position, random.choice(numbers), random.choice(numbers))
