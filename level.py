import json
import os.path
from PIL import Image

from grid import Grid
from grid_item import Dirt

COLORS = {0: None, 100: Dirt}


class Level:
    def __init__(self, grid, title, description):
        self.grid = grid
        self.title = title
        self.description = description


def load_json(path):
    with open(path, "r", encoding="utf8") as json_file:
        data = json.load(json_file)
    return data


def load_level(path):
    info = load_json(os.path.join(path, "info.json"))

    img = Image.open(os.path.join(path, "level.png"))
    pixels = img.load()
    x, y = img.size

    grid = Grid(x, y)

    for i in range(x):
        for j in range(y):
            print(pixels[i, j])
            grid.set_item(i, j, COLORS.get(pixels[i, j], None))

    grid.rendered = grid.render()

    return Level(grid, info["title"], info["description"])
