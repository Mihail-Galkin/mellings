import pygame


class MellingChanger(pygame.sprite.Sprite):
    """
    Спрайт для выбора профессии меллинга, хранящий в себе класс профессии
    """
    def __init__(self, screen, image: pygame.Surface, melling_class, m=1):
        super().__init__(screen.game_sprites, screen.melling_changers_group)
        image_size = image.get_size()
        self.image = pygame.transform.scale(image, (image_size[0] / 2 * m, image_size[1] / 2 * m))
        self.rect = self.image.get_rect()
        self.melling_class = melling_class
