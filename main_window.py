import pygame
from pygame import QUIT

from game import Window

from utilities import tile_texture, stamp

SIZE = 500, 500
FPS = 60


class MainWindow(Window):
    def __init__(self, title, size):
        super().__init__(title, size)

    def start(self):
        from grid import Grid
        from grid_item import Dirt
        from characters import Digger, Floater, Climber, Basher, Miner, Bomber, Builder
        from abstract_characters import MovableCharacter

        self.grid = Grid(180, 180)
        self.players_group = pygame.sprite.Group()
        self.players = [Builder(self.players_group, self, (100, 100))]

        for i in range(170, 180):
            for j in range(0, 180):
                self.grid.set_item(i, j, Dirt(self.grid, (i, j)))
        for i in range(120, 180):
            for j in range(0, 180):
                self.grid.set_item(j, i, Dirt(self.grid, (j, i)))
        for i in range(10):
            for j in range(0, 180):
                self.grid.set_item(i, j, Dirt(self.grid, (i, j)))
        self.grid.rendered = self.grid.render()

        self.colliders = []

    def update(self):
        self.fps = self.clock.get_fps()
        if self.fps == 0:
            return
        self.screen.fill((0, 0, 0))
        self.grid.draw(self.screen)
        self.players_group.draw(self.screen)
        self.players_group.update()

        # print(self.clock.get_fps())

    # def event(self, event):
    #     # from player import Player
    #     # if event.type == pygame.MOUSEBUTTONDOWN:
    #     #     Player(self.players_group, event.pos)
    #     return


if __name__ == "__main__":
    main = MainWindow("123", SIZE)
