import pygame


class MaskCollider(pygame.sprite.Sprite):
    """
    Спрайт, с маской из surface
    """
    def __init__(self, surface: pygame.Surface):
        super().__init__()
        self.image = surface
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)


class BoxCollider(pygame.sprite.Sprite):
    """
    Спрайт представляющий прямоугольник
    """
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill("red")
        self.rect = pygame.Rect(x, y, w, h)

    def resize(self, scale: tuple[int, int]) -> None:
        self.image = pygame.transform.scale(self.image, scale)
        self.rect.width, self.rect.height = scale
