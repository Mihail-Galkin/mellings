import pygame

from utilities import cut_sheet


class Animation:
    def __init__(self, animation_sheet: pygame.Surface, shape: tuple[int, int]):
        self.frames = cut_sheet(animation_sheet, *shape)
        self.flipped_frames = [pygame.transform.flip(i, flip_y=False, flip_x=True) for i in self.frames]
        self.frames_count = len(self.frames)
        self.current_frame = 0

        self.flipped = False

    def apply(self, sprite: pygame.sprite.Sprite):
        if self.flipped:
            sprite.image = self.flipped_frames[self.current_frame]
        else:
            sprite.image = self.frames[self.current_frame]

    def next_frame(self):
        self.current_frame = (self.current_frame + 1) % self.frames_count

    def scale(self, new_scale: tuple[int, int]):
        self.frames = [pygame.transform.scale(i, new_scale) for i in self.frames]
        self.flipped_frames = [pygame.transform.scale(i, new_scale) for i in self.flipped_frames]
