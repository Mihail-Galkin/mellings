import json
import os.path

import numpy
from PIL import Image

from grid import Grid
from grid_item import Dirt
from utilities import load_image

COLORS = {100: Dirt}


class Level:
    def __init__(self, image, img_path, title, description):
        self.img_path = img_path
        self.title = title
        self.description = description
        self.image = image

    def get_grid(self):
        img = Image.open(self.img_path)
        pixels = img.load()

        x, y = img.size

        grid = Grid(x, y)

        for i in range(x):
            for j in range(y):
                grid.set_item(i, j, COLORS[pixels[i, j][0]](grid, (i, j)) if pixels[i, j][0] in COLORS else None)

        grid.update_render()
        return grid


def load_json(path):
    with open(path, "r", encoding="utf8") as json_file:
        data = json.load(json_file)
    return data


def load_level(path: str, title: str):
    info = load_json(os.path.join(path, title + ".json"))

    return Level(load_image(title + ".png", path=path), os.path.join(path, title + ".png"), info["title"], info["description"])
