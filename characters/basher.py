from animation import Animation
from characters.abstract_characters import MovableCharacter
from grid.grid import draw_circle
from utilities import load_image


class Basher(MovableCharacter):
    radius = 5

    def __init__(self, *args, **kwargs):
        self.current_animation = Animation(load_image("bash.png"), (16, 1))
        self.animations = (self.current_animation,)

        super().__init__(*args, **kwargs)

        self.current_cooldown = 0
        self.cooldown = 3

    def custom_update(self):
        self.current_cooldown += 1 / self.game.fps
        if self.current_cooldown >= self.cooldown and self.on_ground:
            self.current_cooldown = 0
            pos = self.rect.midright if self.move_direction == 1 else self.rect.midleft
            pos = self.screen.grid.local_coord(pos)
            draw_circle(self.screen.grid, pos, self.radius, None)

    def wall_reaction(self, direction):
        return
