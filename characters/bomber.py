import math

from animation import Animation
from characters.abstract_characters import MovableCharacter
from grid.grid import draw_circle
from ui.text import draw_text
from utilities import load_image


class Bomber(MovableCharacter):
    radius = 10

    def __init__(self, *args, **kwargs):
        self.current_animation = Animation(load_image("walk.png"), (9, 1))
        self.animations = (self.current_animation,)

        super().__init__(*args, **kwargs)

        self.time_left = 5

    def custom_update(self):
        draw_text(self.screen.layers["gui"][0], (self.rect.x, self.rect.y - 10), str(math.ceil(self.time_left)), 10,
                  (255, 255, 255))
        self.time_left -= 1 / self.game.fps
        if self.time_left <= 0:
            pos_global = self.position[0] + self.rect.width // 2, self.position[1] + self.rect.height // 2
            pos = self.screen.grid.local_coord(pos_global)
            draw_circle(self.screen.grid, pos, self.radius, None)
            from particle import create_particles
            create_particles(self.screen, load_image("data/grid_textures/deepslate.png", path=""), pos_global)

            self.kill()
            self.ground_checker.kill()
            self.screen.players.pop(self)
            