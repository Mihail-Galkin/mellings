import pygame
from pygame.sprite import Sprite, AbstractGroup
from pygame.surface import Surface

from level import Level
from screens.abstract_screen import Screen
from screens.changescreen import change_screen
from screens.game_screen import GameScreen


class LevelWidget(Sprite):
    def __init__(self, screen: Screen, level: Level, size: tuple[int, int], indent: int, color: tuple[int, int, int] = (100, 100, 100), text_size: int = 5):
        super().__init__(screen.gui_sprites)
        self.screen = screen
        self.level = level
        self.image = Surface(size)
        self.rect = pygame.Rect(0, 0, *size)
        self.image.fill(color)

        font = pygame.font.Font(None, text_size)
        text = font.render(level.title, True, (0, 0, 0))
        self.image.blit(text, (indent, size[1] - indent - text.get_height()))

        self.image.blit(pygame.transform.scale(level.image, (size[0] - 2 * indent, size[1] - 3 * indent - text.get_height())), (indent, indent))
        self.clicked = True

    def update(self):
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False
        if self.rect.collidepoint(*pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and not self.clicked:
            change_screen(self.screen.game, GameScreen(self.screen.game, self.level))

