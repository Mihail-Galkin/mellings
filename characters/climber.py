from animation import Animation
from characters.abstract_characters import MovableCharacter
from colliders import BoxCollider
from utilities import load_image
from vector import Vector


class Climber(MovableCharacter):
    climb_speed = 5

    def __init__(self, *args, **kwargs):
        self.walk_animation = Animation(load_image("walk.png"), (9, 1))
        self.climb_animation = Animation(load_image("climb.png"), (10, 1))
        self.current_animation = self.walk_animation
        self.animations = (self.walk_animation, self.climb_animation)

        super().__init__(*args, **kwargs)

        self.is_climbing = False
        self.wall_checker = None

        self.default_g = self.g
        self.default_walk_speed = self.walk_speed

    def custom_update(self):
        if self.is_climbing:
            self.add_velocity("climb", Vector(0, -self.climb_speed))

            self.velocities["g"] = Vector(0, 0)
            self.velocities["walk"] = Vector(0, 0)
            self.forces["g"] = Vector(0, 0)

            self.wall_checker[0].rect.y = self.rect.y - 1
            self.wall_checker[1].rect.y = self.rect.y - 1

            if not self.screen.is_collide(self.wall_checker[0]) or self.screen.is_collide(self.wall_checker[1]):
                self.is_climbing = False

                if not self.screen.is_collide(self.wall_checker[0]):
                    self.rect.x += 1
                    self.position[0] = self.rect.x
                if self.screen.is_collide(self.wall_checker[1]):
                    self.move_direction *= -1

                self.walk_speed = self.default_walk_speed

                self.wall_checker[0].kill()
                self.wall_checker[1].kill()

                self.wall_checker = None
                self.velocities["climb"] = Vector(0, 0)

                self.position = [self.rect.x, self.rect.y]

                self.g = self.default_g

                self.current_animation = self.walk_animation

    def wall_reaction(self, direction):
        height = self.get_wall_height(direction)

        if height < self.jump_height * self.screen.grid.cell_size:
            self.position[1] -= height
            self.position[0] += direction

            self.rect.x, self.rect.y = self.position
        else:
            self.is_climbing = True
            self.add_velocity("climb", Vector(0, -self.climb_speed))
            self.velocities["walk"] = Vector(0, 0)

            self.velocities["g"] = Vector(0, 0)
            self.forces["g"] = Vector(0, 0)

            self.walk_speed = 0
            self.g = 0

            if direction == 1:
                self.wall_checker = (BoxCollider(self.rect.x + self.rect.width, self.rect.y, 1, self.rect.height),
                                     BoxCollider(self.rect.x, self.rect.y, self.rect.width, self.rect.height))
            else:
                self.wall_checker = (BoxCollider(self.rect.x - 1, self.rect.y, 1, self.rect.height),
                                     BoxCollider(self.rect.x, self.rect.y, self.rect.width, self.rect.height))
            self.screen.camera_movable.add(self.wall_checker)
            self.current_animation = self.climb_animation
