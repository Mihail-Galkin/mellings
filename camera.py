import pygame


class Camera:
    def __init__(self):
        self.delta = (0, 0)
        self.size = 2

    def move(self, x: int, y: int) -> None:
        self.delta = self.delta[0] + x, self.delta[1] + y

    def resize(self, delta: int) -> None:
        if delta + self.size > 0:
             self.size += delta

    def apply(self, surface: pygame.Surface):
        new = pygame.transform.scale(surface, (surface.get_width() * self.size, surface.get_height() * self.size))
        surface.fill("black")
        surface.blit(new, self.position)