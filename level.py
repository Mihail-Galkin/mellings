import json
import os.path

import numpy
from PIL import Image

from grid import Grid
from grid_item import Dirt
from utilities import load_image

COLORS = {100: Dirt}


class Level:
    def __init__(self, path, filename, info):
        self.img_path = os.path.join(path, filename + ".png")
        self.image = load_image(filename + ".png", path=path)
        self.title = info["title"]
        self.count = info["count"]
        self.complete_count = info["complete_count"]
        self.spawn = tuple(info["spawn"])
        self.end = tuple(info["end"])
        self.spawn_cooldown = info["spawn_cooldown"]

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


def load_level(path: str, filename: str):
    info = load_json(os.path.join(path, filename + ".json"))

    return Level(path, filename, info)
