import copy
import sys

import pygame

from camera import Camera
from characters.abstract_characters import StaticCharacter
from characters.basher import Basher
from characters.blocker import Blocker
from characters.bomber import Bomber
from characters.builder import Builder
from characters.change_character import change_character
from characters.climber import Climber
from characters.default import DefaultCharacter
from characters.digger import Digger
from characters.floater import Floater
from characters.miner import Miner

from level import Level
from main_window import MainWindow
from screens.abstract_screen import Screen
from screens.changescreen import change_screen
from screens.end_screen import EndScreen
from ui.button import Button
from ui.lemming_button import LemmingButton


class GameScreen(Screen):
    g = 1000

    def __init__(self, game: MainWindow, level: Level):
        self.level = level
        super().__init__(game)

    def start(self):
        from screens.main_menu_screen import MainMenuScreen
        self.back = Button(self, "button.png", (20, 20), change_screen, size=(80, 30), text="Выйти",
                           hover_texture="hover.png", args=[self.game, MainMenuScreen(self.game)])

        self.grid = self.level.get_grid()
        self.layers["game"] = (copy.copy(self.grid.get_surface()), (0, 0))

        self.players = {}

        self.grid.update_collider()

        self.current_button = None
        self.draw_buttons()

        self.size_multiplier = 1

        self.spawn_cooldown = self.level.spawn_cooldown
        self.current_cooldown = 0

        self.spawn_count = self.level.count
        self.characters_complete = 0

    def update(self):
        if not self.spawn_count and self.players == {}:
            change_screen(self.game, EndScreen(self.game, self.characters_complete, self.level.count))

        self.layers["gui"] = (pygame.Surface(self.game.size, pygame.SRCALPHA, 32).convert_alpha(), (0, 0))
        self.layers["game"] = (copy.copy(self.grid.get_surface()), self.layers["game"][1])

        self.current_cooldown += 1 / self.game.fps
        if self.current_cooldown >= self.spawn_cooldown and self.spawn_count:
            self.current_cooldown = 0
            self.spawn_count -= 1
            self.players[DefaultCharacter(self, (
                self.level.spawn[0] * self.grid.cell_size, self.level.spawn[1] * self.grid.cell_size),
                                          size=self.size_multiplier)] = -1

        for i in self.players:
            if self.players[i] == -1:
                continue
            elif -1 < self.players[i] < 0:
                change_character(i, DefaultCharacter, -1)
            else:
                self.players[i] -= 1 / self.game.fps

        delta = [0, 0]
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            delta[1] -= 1
        if keys[pygame.K_UP]:
            delta[1] += 1
        if keys[pygame.K_LEFT]:
            delta[0] += 1
        if keys[pygame.K_RIGHT]:
            delta[0] -= 1
        self.layers["game"] = (
            self.layers["game"][0], (self.layers["game"][1][0] + delta[0], self.layers["game"][1][1] + delta[1]))

        for i in self.players_group.sprites():
            if i.rect.collidepoint(self.level.end[0] * self.grid.cell_size, self.level.end[1] * self.grid.cell_size):
                self.characters_complete += 1
                i.kill()
                self.players.pop(i)
            if i.rect.collidepoint(pygame.mouse.get_pos()[0] - self.layers["game"][1][0],
                                   pygame.mouse.get_pos()[1] - self.layers["game"][1][1]):
                pygame.draw.rect(self.layers["game"][0], "yellow", i.rect, 3)

                if isinstance(i, DefaultCharacter) and self.current_button and pygame.mouse.get_pressed()[0]:
                    change_character(i, self.current_button.lemming_class, 5000)
                break

        self.gui_sprites.draw(self.layers["gui"][0])
        self.game_sprites.draw(self.layers["game"][0])

        self.gui_sprites.update()
        self.game_sprites.update()

    def event(self, events: list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.MOUSEWHEEL:
                if event.y == 1:
                    m = 2
                else:
                    m = 0.5
                self.size_multiplier *= m

                for i in self.game_sprites.sprites():
                    if isinstance(i, StaticCharacter):
                        i.resize((i.rect.width * m, i.rect.height * m))
                self.grid.set_cell_size(int(self.grid.cell_size * m))

    def draw_buttons(self):
        buttons_title = ["basher", "blocker", "bomber", "builder", "climber", "digger", "floater", "miner"]  # const
        buttons_class = [Basher, Blocker, Bomber, Builder, Climber, Digger, Floater, Miner]
        self.buttons = [
            LemmingButton(self, f"buttons\\{buttons_title[i]}.jpg", buttons_class[i], (i * 32, self.game.size[1] - 40),
                          self.change_selected, arg=i) for i in range(len(buttons_title))]

        self.boom_button = Button(self, "buttons\\bomb.jpg", (8 * 32, self.game.size[1] - 40),
                                  lambda: [change_character(i, Bomber, -1) for i in self.players_group.sprites()])

    def change_selected(self, game: MainWindow, index: int):
        b = self.buttons[index].activated
        for i in self.buttons:
            i.set_activated(False)
        self.buttons[index].set_activated(not b)
        if not b:
            self.current_button = self.buttons[index]
        else:
            self.current_button = None

    def is_collide(self, sprite):
        collider = self.grid.get_collider()
        return bool(pygame.sprite.collide_mask(sprite, collider) or pygame.sprite.spritecollide(sprite, self.blockers,
                                                                                                dokill=False))
