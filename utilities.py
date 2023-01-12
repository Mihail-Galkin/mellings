import os
import sys

import pygame


def load_image(name: str, colorkey=None, path: str="data") -> pygame.Surface:
    fullname = os.path.join(path, name)
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


def tile_texture(texture: pygame.Surface, size: tuple[int, int]) -> pygame.Surface:
    """
    Функция равномерно заполняет поверхность заданного размера текстурой
    """
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


def cut_sheet(sheet: pygame.Surface, columns: int, rows: int) -> list[pygame.Surface]:
    frames = []
    rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
    for j in range(rows):
        for i in range(columns):
            frame_location = (rect.w * i, rect.h * j)
            frames.append(sheet.subsurface(pygame.Rect(frame_location, rect.size)))
    return frames


