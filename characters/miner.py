from animation import Animation
from characters.abstract_characters import MovableCharacter
from grid.grid import draw_circle
from utilities import load_image


class Miner(MovableCharacter):

    def __init__(self, *args, **kwargs):
        self.current_animation = Animation(load_image("mine.png"), (7, 1))
        self.animations = (self.current_animation,)

        super().__init__(*args, **kwargs)

        self.current_cooldown = 3
        self.cooldown = 3

        self.radius = 7

    def custom_update(self):
        self.current_cooldown += 1 / self.game.fps
        if self.current_cooldown >= self.cooldown and self.on_ground:
            self.current_cooldown = 0
            pos = self.position[0] + (self.rect.width if self.move_direction == 1 else 0), self.position[1] + self.rect.height // 4 * 3
            pos = self.screen.grid.local_coord(pos)
            draw_circle(self.screen.grid, pos, self.radius, None)

    def wall_reaction(self, direction):
        return