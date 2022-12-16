import pygame
from pygame import QUIT

from game import Window

from utilities import tile_texture, stamp

SIZE = 500, 500
FPS = 600


class MainWindow(Window):
    def __init__(self, title, size, fps):
        super().__init__(title, size, fps)

    def start(self):
        from grid import Grid, Dirt
        from player import Player, Digger

        self.grid = Grid(180, 180)
        self.players_group = pygame.sprite.Group()
        self.players = [Digger(self.players_group, self.grid)]

        for i in range(170, 180):
            for j in range(0, 180):
                self.grid.set_item(i, j, Dirt(self.grid, (i, j)))
        for i in range(170, 180):
            for j in range(0, 180):
                self.grid.set_item(j, i, Dirt(self.grid, (j, i)))
        for i in range(10):
            for j in range(0, 180):
                self.grid.set_item(i, j, Dirt(self.grid, (i, j)))
        self.grid.rendered = self.grid.render()

    def update(self):
        self.screen.fill((0, 0, 0))
        self.grid.draw(self.screen)
        self.players_group.draw(self.screen)
        self.players[0].update()

        # print(self.clock.get_fps())

    # def event(self, event):
    #     # from player import Player
    #     # if event.type == pygame.MOUSEBUTTONDOWN:
    #     #     Player(self.players_group, event.pos)
    #     return


if __name__ == "__main__":
    main = MainWindow("123", SIZE, FPS)
