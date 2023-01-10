import csv
import json
import os.path

from PIL import Image

from grid.grid import Grid
from grid.grid_item import GridItem
from utilities import load_image


class Level:
    def __init__(self, path, filename, info, completed):
        self.filename = filename
        self.img_path = os.path.join(path, filename + ".png")
        self.image = load_image(filename + ".png", path=path)
        self.title = info["title"]
        self.count = info["count"]
        self.complete_count = info["complete_count"]
        self.spawn = tuple(info["spawn"])
        self.end = tuple(info["end"])
        self.spawn_cooldown = info["spawn_cooldown"]
        self.completed = completed
        self.buttons_count = info["buttons_count"]

    def get_grid(self):
        colors = {}
        with open('data/grid_textures/colors.csv', encoding="utf8") as csvfile:
            reader = list(csv.reader(csvfile, delimiter=',', quotechar='"'))[1:]
            for texture, r, g, b in reader:
                colors[(int(r), int(g), int(b))] = load_image(texture, path="data/grid_textures/")
        print(colors)

        img = Image.open(self.img_path)
        pixels = img.load()
        x, y = img.size

        grid = Grid(x, y)

        for i in range(x):
            for j in range(y):
                color = pixels[i, j] if len(pixels[i, j]) == 3 else pixels[i, j][:3]
                if color in colors:
                    item = GridItem(grid, (i, j))
                    item.texture = colors[color]
                else:
                    item = None
                grid.set_item(i, j, item)

        grid.update_render()
        return grid


def load_json(path):
    with open(path, "r", encoding="utf8") as json_file:
        data = json.load(json_file)
    return data


def load_level(path: str, filename: str, completed: bool = False):
    info = load_json(os.path.join(path, filename + ".json"))

    return Level(path, filename, info, completed)
