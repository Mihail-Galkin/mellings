import pygame

from game import Window

from utilities import tile_texture, stamp

SIZE = 500, 500
FPS = 60


class MainWindow(Window):
    def __init__(self, title, size):
        super().__init__(title, size)

    def start(self):
        from grid import Grid, Dirt
        from player import Player

        self.grid = Grid(180, 180)
        self.players_group = pygame.sprite.Group()
        self.players = [Player(self.players_group, self.grid)]



        for i in range(90, 180):
            for j in range(0, 180):
                self.grid.board[j, i] = Dirt(self.grid, (j, i))
        print(self.grid.board)

    def update(self):
        self.screen.fill((0, 0, 0))
        self.grid.render(self.screen)
        self.players_group.draw(self.screen)
        self.players[0].update()

    # def event(self, event):
    #     # from player import Player
    #     # if event.type == pygame.MOUSEBUTTONDOWN:
    #     #     Player(self.players_group, event.pos)
    #     return

if __name__ == "__main__":
    main = MainWindow("123", SIZE)
