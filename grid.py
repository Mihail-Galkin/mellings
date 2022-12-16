import numpy as np
import pygame

import utilities
from grid_item import GridItem
from main_window import SIZE


class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = np.array([[None for i in range(height)] for j in range(width)])
        self.left = 10
        self.top = 10
        self.cell_size = 2
        self.mask = self.compute_mask()
        self.rendered = self.render()

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def draw(self, screen):
        screen.blit(self.rendered, (0, 0))

    def render(self):
        result = pygame.Surface(SIZE, pygame.SRCALPHA, 32)
        result.convert_alpha()

        mask = self.get_mask()
        print(mask)
        for i in mask:
            texture = utilities.tile_texture(i, SIZE)
            utilities.stamp(result, texture, mask[i])
        return result

    def to_local_coordinates(self, coord):
        return (coord[0] - self.left) // self.cell_size, (coord[1] - self.top) // self.cell_size

    def to_absolute_coordinates(self, coord):
        return self.left + coord[0] * self.cell_size, self.top + coord[1] * self.cell_size

    def get_mask(self):
        return self.mask

    def compute_mask(self):
        masks = {}
        for i in range(self.width):
            for j in range(self.height):
                if self.board[i, j] is None:
                    continue
                if self.board[i, j].texture not in masks.keys():
                    masks[self.board[i, j].texture] = pygame.Surface(SIZE, depth=8)
                self.board[i, j].render(masks[self.board[i, j].texture])
        return masks

    def set_item(self, x: int, y: int, item: GridItem):
        old = self.board[x, y]
        if old is not None:
            pygame.draw.rect(self.mask[old.texture], 0, (*self.to_absolute_coordinates((x, y)), self.cell_size, self.cell_size))
        if item is not None:
            if item.texture not in self.mask.keys():
                self.mask[item.texture] = pygame.Surface(SIZE, depth=8)
            item.render(self.mask[item.texture])
        self.board[x, y] = item

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

    def get_collider(self):
        surface = pygame.Surface(SIZE, pygame.SRCALPHA, 32)
        surface = surface.convert_alpha()

        self.draw(surface)
        return MaskCollider(surface)


class MaskCollider(pygame.sprite.Sprite):
    def __init__(self, surface):
        super().__init__()
        self.image = surface
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)


class BoxCollider(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill("red")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Dirt(GridItem):
    texture = utilities.load_image("dirt.png")

    def __init__(self, grid: Grid, position: tuple):
        super().__init__(grid, position)
