from animation import Animation
from characters.abstract_characters import MovableCharacter
from grid import draw_circle
from utilities import load_image


class Digger(MovableCharacter):
    radius = 6


    def __init__(self, *args, **kwargs):
        self.current_animation = Animation(load_image("dig.png"), (8, 1))
        self.animations = (self.current_animation,)

        super().__init__(*args, **kwargs)

        self.current_cooldown = 0
        self.cooldown = 3

        self.walk_speed = 0

    def custom_update(self):
        self.current_cooldown += 1 / self.game.fps
        if self.current_cooldown >= self.cooldown and self.on_ground:
            self.current_cooldown = 0
            pos = self.rect.midbottom
            pos = self.screen.grid.local_coord(pos)
            draw_circle(self.screen.grid, pos, self.radius, None)