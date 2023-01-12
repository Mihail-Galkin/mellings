from animation import Animation
from characters.abstract_characters import MovableCharacter
from utilities import load_image
from vector import Vector


class Floater(MovableCharacter):

    def __init__(self, *args, **kwargs):
        self.walk_animation = Animation(load_image("walk.png"), (9, 1))
        self.float_animation = Animation(load_image("float.png"), (3, 1))
        self.current_animation = self.walk_animation
        self.animations = (self.walk_animation, self.float_animation)

        super().__init__(*args, **kwargs)
        self.max_fall_velocity = 10 ** 5

    def custom_update(self):
        if self.on_ground:
            self.current_animation = self.walk_animation
        else:
            self.current_animation = self.float_animation
