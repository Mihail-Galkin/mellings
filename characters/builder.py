from animation import Animation
from characters.abstract_characters import MovableCharacter
from characters.change_character import change_character
from characters.default import DefaultCharacter
from grid_item import Stairs
from utilities import load_image


class Builder(MovableCharacter):
    platform_size = 3

    def __init__(self, *args, **kwargs):
        self.current_animation = Animation(load_image("walk.png"), (9, 1))
        self.animations = (self.current_animation,)

        super().__init__(*args, **kwargs)
        self.animations = (self.current_animation,)
        self.cooldown = 0
        self.cooldown_max = 1
        self.first_placed = False

        self.walk_speed //= 8

    def custom_update(self):
        if not self.first_placed and self.on_ground:
            self.build(self.move_direction)
            self.first_placed = True

    def wall_reaction(self, direction):
        height = self.get_wall_height(direction)
        if height < self.jump_height * self.screen.grid.cell_size:
            self.position[1] -= height
            self.position[0] += direction

            self.rect.x, self.rect.y = self.position

            self.build(direction)
        else:
            self.move_direction = -direction
            change_character(self, DefaultCharacter, -1)

    def build(self, direction):
        pos = self.rect.x + self.rect.width + self.platform_size, self.rect.height + self.rect.y
        pos = list(map(int, self.screen.grid.local_coord(pos)))

        for i in range(self.platform_size):
            new = pos[:]
            new[0] += i * int(direction)
            new[1] -= 1
            self.screen.grid.set_item(*new, Stairs(self.screen.grid, tuple(new)))

        self.screen.grid.update_render()
        self.screen.grid.update_collider()
