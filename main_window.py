from game import Window
from utilities import tile_texture, stamp

SIZE = 500, 500


class MainWindow(Window):
    def __init__(self, title, size):
        super().__init__(title, size)

    def start(self):
        from grid import Grid
        self.grid = Grid(180, 180)

    def update(self):
        self.screen.fill((0, 0, 0))
        self.grid.render(self.screen)


if __name__ == "__main__":
    main = MainWindow("123", SIZE)
