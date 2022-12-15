import os
import random
import sys
from math import sqrt

import pygame


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def tile_texture(texture, size):
    # Равномерно заполняет поверхность текстурой
    result = pygame.Surface(size, depth=32)
    for x in range(0, size[0], texture.get_width()):
        for y in range(0, size[1], texture.get_height()):
            result.blit(texture, (x, y))
    return result


def apply_alpha(texture: pygame.Surface, mask: pygame.Surface):
    texture = texture.convert_alpha()
    target = pygame.surfarray.pixels_alpha(texture)
    target[:] = pygame.surfarray.array2d(mask)
    del target
    return texture


def stamp(image, texture, mask):
    image.blit(apply_alpha(texture, mask), (0, 0))
