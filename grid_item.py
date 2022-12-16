import pygame


class GridItem:
    texture = ""

    def __init__(self, grid, position: tuple):
        self.position = position
        self.grid = grid

    def render(self, screen):
        pygame.draw.rect(screen, 255, self.grid.to_absolute_coordinates(self.position) + (self.grid.cell_size,) * 2)
