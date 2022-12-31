from typing import Callable

import pygame

from main_window import MainWindow
from screens.abstract_screen import Screen
from utilities import load_image


class Button(pygame.sprite.Sprite):
    def __init__(self, screen: Screen, texture: str,
                 position: tuple[int, int], listener: Callable[[MainWindow], None],
                 size: tuple[int, int] = None, text: str = "", text_color="white",
                 text_size: int = 20, hover_texture: str = None):
        super().__init__(screen.all_sprites)
        screen.buttons_group.add(self)

        if size is not None:
            self.default_image = pygame.transform.scale(load_image(texture), size)
            self.hover_image = pygame.transform.scale(load_image(hover_texture), size)
        else:
            self.default_image = load_image(texture)
            self.hover_image = load_image(hover_texture)
        self.image = self.default_image

        self.rect = self.image.get_rect()
        self.listener = listener
        self.game = screen.game
        self.screen = screen
        self.text = text
        self.text_color = text_color
        self.text_size = text_size

        self.clicked = False

        self.rect.x, self.rect.y = position

    def update(self):
        if self.hover_image and self.rect.collidepoint(*pygame.mouse.get_pos()):
            self.image = self.hover_image
        else:
            self.image = self.default_image

        self.draw_text()
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False
        if self.rect.collidepoint(*pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and not self.clicked:
            self.listener(self.game)
            self.clicked = True

    def draw_text(self):
        font = pygame.font.Font(None, self.text_size)
        text = font.render(self.text, True, self.text_color)

        text_scale = (text.get_width(), text.get_height())

        self.game.surface.blit(text,
                               (self.rect.x + (self.rect.width - text_scale[0]) // 2,
                                self.rect.y + (self.rect.height - text_scale[1]) // 2))
