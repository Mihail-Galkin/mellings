from typing import Callable

import pygame

from main_window import MainWindow
from screens.abstract_screen import Screen
from utilities import load_image


class Button(pygame.sprite.Sprite):
    def __init__(self, screen: Screen, texture: str,
                 position: tuple[int, int], listener: Callable[[...], None],
                 size: tuple[int, int] = None, text: str = "", text_color="dimgray",
                 text_size: int = 20, hover_texture: str = None, args=None, kwargs=None):
        super().__init__(screen.gui_sprites)

        if kwargs is None:
            kwargs = {}
        if args is None:
            args = []

        self.kwargs = kwargs
        self.args = args

        if size is not None:
            self.default_image = pygame.transform.scale(load_image(texture), size)
            if hover_texture:
                self.hover_image = pygame.transform.scale(load_image(hover_texture), size)
            else:
                self.hover_image = None
        else:
            self.default_image = load_image(texture)
            if hover_texture:
                self.hover_image = load_image(hover_texture)
            else:
                self.hover_image = None
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

        self.texture = texture

    def update(self):
        if self.hover_image and self.rect.collidepoint(*pygame.mouse.get_pos()):
            self.image = self.hover_image
        else:
            self.image = self.default_image

        self.draw_text()
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False
        if self.rect.collidepoint(*pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and not self.clicked:
            self.listener(*self.args, **self.kwargs)
            self.clicked = True

    def draw_text(self):
        font = pygame.font.Font("data\\pixelfont_7.ttf", self.text_size)
        text = font.render(self.text, True, self.text_color)

        text_scale = (text.get_width(), text.get_height())

        self.screen.layers["gui"][0].blit(text,
                                       (self.rect.x + (self.rect.width - text_scale[0]) // 2,
                                        self.rect.y + (self.rect.height - text_scale[1]) // 2))
