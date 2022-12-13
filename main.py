import random
import time

import pygame

from utilities import tile_texture, stamp


# SIZE = 800, 600


def main():
    pygame.init()
    pygame.display.set_caption('Mellings')
    screen = pygame.display.set_mode(SIZE)

    from grid import Grid, Dirt
    grid = Grid(180, 180)
    running = True
    while running:
        screen.fill((0, 0, 0))
        for texture in grid.get_mask():
            t = tile_texture(texture, SIZE)
            stamp(screen, t, grid.get_mask()[texture])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                grid.get_click(pos)
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    try:
        main()
    finally:
        pygame.quit()
