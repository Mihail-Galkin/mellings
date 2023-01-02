import copy
import sys

import pygame

from camera import Camera
from characters.change_character import change_character
from characters.character import Builder, Floater, Basher, Blocker, Bomber, Climber, Digger, Miner

from level import Level
from main_window import MainWindow
from screens.abstract_screen import Screen
from ui.button import Button
from ui.lemming_button import LemmingButton


class GameScreen(Screen):
    def __init__(self, game: MainWindow, level: Level):
        self.level = level
        super().__init__(game)

    def start(self):
        self.grid = self.level.get_grid()
        # self.grid.rendered = self.grid.render()

        self.players = {Builder(self, (100, 100)): 5}

        self.colliders = []

        self.btn = Button(self, "button.png", (100, 100), lambda x: sys.exit(0), size=(50, 20), text="Exit",
                          hover_texture="hover.png")

        self.camera = Camera()

        self.grid.update_collider()

        self.current_button = None
        self.draw_buttons()

    def update(self):
        for i in copy.copy(self.players):
            if self.players[i] == -1:
                continue
            elif int(self.players[i]) == 0:
                change_character(i, Floater, 5)
            else:
                self.players[i] -= 1 / self.game.fps

        self.game.surface.fill((0, 0, 0))

        self.players_group.update()
        self.buttons_group.update()

        delta = [0, 0]
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            delta[1] += 1
        if keys[pygame.K_UP]:
            delta[1] -= 1
        if keys[pygame.K_LEFT]:
            delta[0] -= 1
        if keys[pygame.K_RIGHT]:
            delta[0] += 1

        self.camera.set_delta(*delta)
        for i in self.players_group.sprites():
            self.camera.apply(i)

        if self.camera.delta[0] or self.camera.delta[1]:
            self.grid.set_view(self.grid.left + self.camera.delta[0], self.grid.top + self.camera.delta[1],
                               self.grid.cell_size)

        self.grid.draw(self.game.surface)
        self.all_sprites.draw(self.game.surface)

    def event(self, events: list[pygame.event.Event]):
        lemming = None
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                for i in self.players_group.sprites():
                    if i.rect.collidepoint(*pygame.mouse.get_pos()):
                        lemming = i
                        pygame.draw.rect(self.game.surface, "green", i.rect, 1)
                        break
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in self.players_group.sprites():
                    if i.rect.collidepoint(*pygame.mouse.get_pos()) and self.current_button:

                        change_character(i, self.current_button.lemming_class, 5)



    def draw_buttons(self):
        buttons_title = ["basher", "blocker", "bomber", "builder", "climber", "digger", "floater", "miner"]  # const
        buttons_class = [Basher, Blocker, Bomber, Builder, Climber, Digger, Floater, Miner]
        self.buttons = [LemmingButton(self, f"buttons\\{buttons_title[i]}.jpg", buttons_class[i], (i * 32, 300),
                                      self.change_selected, arg=i) for i in range(len(buttons_title))]

    def change_selected(self, game: MainWindow, index: int):
        ic()
        b = self.buttons[index].activated
        for i in self.buttons:
            i.set_activated(False)
        self.buttons[index].set_activated(not b)
        if not b:
            self.current_button = self.buttons[index]
        else:
            self.current_button = None
