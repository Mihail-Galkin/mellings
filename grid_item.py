import pygame

import utilities
from grid import Grid


class GridItem:
    texture = None

    def __init__(self, grid, position: tuple):
        self.position = position
        self.grid = grid

    def render(self, screen):
        pygame.draw.rect(screen, 255, self.grid.to_absolute_coordinates(self.position) + (self.grid.cell_size,) * 2)


class Dirt(GridItem):
    texture = utilities.load_image("dirt.png")

    def __init__(self, grid: Grid, position: tuple):
        super().__init__(grid, position)


class Stairs(GridItem):
    texture = utilities.load_image("dirt.png")

    def __init__(self, grid: Grid, position: tuple):
        super().__init__(grid, position)
