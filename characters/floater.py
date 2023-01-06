from animation import Animation
from characters.abstract_characters import MovableCharacter
from utilities import load_image
from vector import Vector


class Floater(MovableCharacter):

    def __init__(self, *args, **kwargs):
        self.current_animation = Animation(load_image("walk.png"), (9, 1))
        self.animations = (self.current_animation,)

        super().__init__(*args, **kwargs)

    def custom_update(self):
        if self.on_ground:
            self.forces["umbrella"] = 0
            self.velocities["umbrella"] = 0
        elif "g" in self.velocities.keys():
            self.velocities["umbrella"] = -self.velocities["g"] + Vector(0, 20)
