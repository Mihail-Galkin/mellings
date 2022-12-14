import numpy as np
import pygame

import utilities
from main_window import SIZE


class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = np.array([[None for i in range(height)] for j in range(width)])
        self.left = 10
        self.top = 10
        self.cell_size = 2

        self.mask = self.get_mask()

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        mask = self.get_mask()
        for i in mask:
            texture = utilities.tile_texture(i, SIZE)
            utilities.stamp(screen, texture, mask[i])

    def to_local_coordinates(self, coord):
        return (coord[0] - self.left) // self.cell_size, (coord[1] - self.top) // self.cell_size

    def to_absolute_coordinates(self, coord):
        return self.left + coord[0] * self.cell_size, self.top + coord[1] * self.cell_size

    def get_mask(self):
        masks = {}
        for i in range(self.width):
            for j in range(self.height):
                if self.board[i, j] is None:
                    continue
                if self.board[i, j].texture not in masks.keys():
                    masks[self.board[i, j].texture] = pygame.Surface(SIZE, depth=8)
                self.board[i, j].render(masks[self.board[i, j].texture])
        return masks

    def get_cell(self, mouse_pos: tuple):
        if not (self.left <= mouse_pos[0] <= self.left + self.width * self.cell_size and
                self.top <= mouse_pos[1] <= self.top + self.height * self.cell_size):
            return None
        return (mouse_pos[0] - self.left) // self.cell_size, (mouse_pos[1] - self.top) // self.cell_size

    def get_click(self, mouse_pos: tuple):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def on_click(self, cell_coord: tuple):
        if cell_coord is not None:
            self.board[cell_coord] = Dirt(self, cell_coord)

    def set_item(self, i, j, item):
        self.board[i, j] = item

    def get_collider(self):
        surface = pygame.Surface(SIZE, pygame.SRCALPHA, 32)
        surface = surface.convert_alpha()

        self.render(surface)
        return Collider(surface)


class Collider(pygame.sprite.Sprite):
    def __init__(self, surface):
        super().__init__()
        self.image = surface
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)


class GridItem:
    def __init__(self, grid: Grid, position: tuple):
        self.position = position
        self.grid = grid

    def render(self, screen):
        pygame.draw.rect(screen, 255, self.grid.to_absolute_coordinates(self.position) + (self.grid.cell_size,) * 2)


class Dirt(GridItem):
    texture = utilities.load_image("dirt.png")

    def __init__(self, grid: Grid, position: tuple):
        super().__init__(grid, position)
