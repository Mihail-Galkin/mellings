import copy
from typing import Any

import numpy as np
import pygame

import utilities
from colliders import MaskCollider


class Grid:
    """
    Класс, реализующий игровое поле
    """
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.board = np.array([[None for _ in range(height)] for _ in range(width)])
        self.cell_size = 1
        self.update_mask()
        self.update_render()
        self.update_collider()

    def set_cell_size(self, cell_size: int) -> None:
        self.cell_size = cell_size
        self.update_mask()
        self.update_render()

        self.update_collider()

    def draw(self, screen: pygame.Surface) -> None:
        """
        Накладывает на данную поверхность поле
        """
        screen.blit(self.rendered, (0, 0))

    def get_surface(self) -> pygame.Surface:
        """
        Возвращает текущий вид поля
        """
        return copy.copy(self.rendered)

    def update_render(self) -> None:
        """
        Обновляет текущий вид поля
        """
        result = pygame.Surface((self.cell_size * self.width, self.cell_size * self.height), pygame.SRCALPHA, 32)
        result.convert_alpha()

        mask = self.get_mask()
        for i in mask:
            utilities.stamp(result,
                            utilities.tile_texture(i, (self.cell_size * self.width, self.cell_size * self.height)),
                            mask[i])
        self.rendered = result

    def local_coord(self, coord) -> tuple[int, int]:
        return coord[0] // self.cell_size, coord[1] // self.cell_size

    def global_coord_without_indent(self, coord) -> tuple[int, int]:
        return coord[0] * self.cell_size, coord[1] * self.cell_size

    def get_mask(self) -> dict[pygame.Surface, pygame.Surface]:
        """
        Возвращает маску, необходимую для рендера поля
        """
        return self.mask

    def update_mask(self) -> None:
        """
        Обновляет маску
        """
        masks = {}
        for i in range(self.width):
            for j in range(self.height):
                if self.board[i, j] is None:
                    continue
                if self.board[i, j].texture not in masks.keys():
                    masks[self.board[i, j].texture] = pygame.Surface(
                        (self.cell_size * self.width, self.cell_size * self.height), depth=8)
                self.board[i, j].render(masks[self.board[i, j].texture])
        self.mask = masks

    def set_item(self, x: int, y: int, item) -> None:
        """
        Изменяет материал заданной ячейки
        """
        x = int(x)
        y = int(y)
        if not (0 <= x < self.width and 0 <= y < self.height):
            return
        old = self.board[x, y]
        if old is not None:
            pygame.draw.rect(self.mask[old.texture], 0,
                             (*self.global_coord_without_indent((x, y)), self.cell_size, self.cell_size))
        if item is not None:
            if item.texture not in self.mask.keys():
                self.mask[item.texture] = pygame.Surface((self.cell_size * self.width, self.cell_size * self.height),
                                                         depth=8)
            item.render(self.mask[item.texture])
        self.board[int(x), int(y)] = item

    def get_collider(self) -> MaskCollider:
        return self.collider

    def update_collider(self) -> None:
        surface = pygame.Surface((self.cell_size * self.width, self.cell_size * self.height), pygame.SRCALPHA, 32)
        surface = surface.convert_alpha()

        self.draw(surface)
        self.collider = MaskCollider(surface)


def draw_circle(grid: Grid, position: tuple[int, int], radius: int, material) -> None:
    new = copy.deepcopy(position)
    for i in range(-radius, radius + 1):
        for j in range(-radius, radius + 1):
            if i ** 2 + j ** 2 <= radius ** 2:
                if material:
                    grid.set_item(new[0] + i, new[1] + j, material(grid, position))
                else:
                    grid.set_item(new[0] + i, new[1] + j, None)
    grid.update_render()
    grid.update_collider()
