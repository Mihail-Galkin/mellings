from animation import Animation
from characters.abstract_characters import StaticCharacter
from utilities import load_image


class Blocker(StaticCharacter):

    def __init__(self, *args, **kwargs):
        self.current_animation = Animation(load_image("block.png"), (16, 1))
        self.animations = (self.current_animation,)

        super().__init__(*args, **kwargs)

        self.screen.blockers.add(self)

    def custom_update(self):
        pass
