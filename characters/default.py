from animation import Animation
from characters.abstract_characters import MovableCharacter
from utilities import load_image


class DefaultCharacter(MovableCharacter):
    def __init__(self, *args, **kwargs):
        self.current_animation = Animation(load_image("walk.png"), (9, 1))
        self.animations = (self.current_animation,)

        super().__init__(*args, **kwargs)
