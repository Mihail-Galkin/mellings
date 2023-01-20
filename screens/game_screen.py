import copy
import csv
import os

import pygame

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
from main import MainWindow
from melling_changer import MellingChanger
from screens.abstract_screen import Screen
from screens.change_screen import change_screen
from screens.end_screen import EndScreen
from ui.button import Button
from ui.melling_button import LemmingButton
from utilities import load_image

LEVELS_FOLDER = "level"


class GameScreen(Screen):
    g = 400

    def __init__(self, game: MainWindow, level: Level):
        self.level = level
        super().__init__(game)

    def start(self):
        from screens.main_menu_screen import MainMenuScreen
        self.back = Button(self, "button.png", (20, 20), change_screen, size=(80, 30), text="Выйти",
                           hover_texture="hover.png", args=[self.game, MainMenuScreen(self.game)])

        self.grid = self.level.get_grid()

        # слой с игрой - это grid surface + персонажи
        self.layers["game"] = (copy.copy(self.grid.get_surface()), (0, 0))

        self.players = {}
        self.melling_changers = []

        self.grid.update_collider()

        self.current_button = None  # выбранная кнопка персонажей
        self.draw_buttons()

        self.size_multiplier = 1

        self.spawn_cooldown = self.level.spawn_cooldown
        self.current_cooldown = 0

        self.spawn_count = self.level.count
        self.characters_complete = 0

        # Установка спрайтов начала и конца
        self.spawn_sprite = pygame.sprite.Sprite(self.game_sprites)
        self.spawn_sprite.image = load_image("spawn.png")
        self.spawn_sprite.rect = self.spawn_sprite.image.get_rect()
        self.spawn_sprite.rect.midbottom = (self.level.spawn[0] * self.grid.cell_size,
                                            self.level.spawn[1] * self.grid.cell_size)

        self.end_sprite = pygame.sprite.Sprite(self.game_sprites)
        self.end_sprite.image = load_image("exit.png")
        self.end_sprite.rect = self.spawn_sprite.image.get_rect()
        self.end_sprite.rect.midbottom = (self.level.end[0] * self.grid.cell_size,
                                          self.level.end[1] * self.grid.cell_size)

        self.spawn_default_size = self.spawn_sprite.rect.width, self.spawn_sprite.rect.height
        self.end_default_size = self.end_sprite.rect.width, self.end_sprite.rect.height

    def update(self):
        from screens.mulitiplayer.multiplayer_game_screen import MultiplayerGameScreen
        if not self.spawn_count and self.players == {} and not isinstance(self, MultiplayerGameScreen):
            # Конец игры
            if self.level.complete_count <= self.characters_complete:
                # Изменение информации о том, пройден ли уровень
                with open(os.path.join(LEVELS_FOLDER, "levels.csv"), encoding="utf8") as csvfile:
                    reader = list(csv.reader(csvfile, delimiter=',', quotechar='"'))[1:]
                for i in range(len(reader)):
                    if reader[i][0] == self.level.filename:
                        reader[i] = reader[i][0], 1
                reader = [("level", "completed")] + reader
                with open(os.path.join(LEVELS_FOLDER, "levels.csv"), 'w', newline='', encoding="utf8") as csvfile:
                    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerows(reader)
            change_screen(self.game,
                          EndScreen(self.game, self.characters_complete, self.level.count, self.level.complete_count))

        self.layers["gui"] = (pygame.Surface(self.game.size, pygame.SRCALPHA, 32).convert_alpha(), (0, 0))
        self.layers["game"] = (copy.copy(self.grid.get_surface()), self.layers["game"][1])

        # Спавн игроков
        self.current_cooldown += 1 / self.game.fps
        if self.current_cooldown >= self.spawn_cooldown and self.spawn_count:
            self.current_cooldown = 0
            self.spawn_count -= 1
            self.players[DefaultCharacter(self, (
                self.level.spawn[0] * self.grid.cell_size, self.level.spawn[1] * self.grid.cell_size),
                                          size=self.size_multiplier)] = -1

        # Уменьшение кулдауна персонажей
        to_change = []
        for i in self.players:
            if self.players[i] == -1:
                continue
            elif -1 < self.players[i] < 0:
                to_change.append(i)
            else:
                self.players[i] -= 1 / self.game.fps
        for i in to_change:
            change_character(i, DefaultCharacter, -1)

        # Движение камеры
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
        self.layers["game"] = (self.layers["game"][0],
                               (self.layers["game"][1][0] + delta[0], self.layers["game"][1][1] + delta[1]))

        for i in self.players_group.sprites():
            if i.rect.collidepoint(self.level.end[0] * self.grid.cell_size, self.level.end[1] * self.grid.cell_size):
                self.characters_complete += 1
                i.kill()
                self.players.pop(i)

        self.gui_sprites.draw(self.layers["gui"][0])
        self.game_sprites.draw(self.layers["game"][0])

        self.gui_sprites.update()
        self.game_sprites.update()

        self.custom_update()

    def custom_update(self):
        return

    def event(self, events: list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.MOUSEWHEEL:
                # Модификация масштаба
                if event.y == 1:
                    m = 2
                    if self.size_multiplier == 4:
                        return
                else:
                    m = 0.5
                    if self.size_multiplier == 1:
                        return
                self.size_multiplier *= m

                for i in self.game_sprites.sprites():
                    if isinstance(i, StaticCharacter):
                        i.resize((i.rect.width * m, i.rect.height * m))
                    elif i is not self.spawn_sprite and i is not self.end_sprite:
                        i.rect.x = int(i.rect.x * m)
                        i.rect.y = int(i.rect.y * m)
                        i.rect.width = int(i.rect.width * m)
                        i.rect.height = int(i.rect.height * m)
                        i.image = pygame.transform.scale(i.image, i.rect.size)

                self.grid.set_cell_size(int(self.grid.cell_size * m))

                # Изменение позиции начала и конца
                self.spawn_sprite.image = pygame.transform.scale(self.spawn_sprite.image,
                                                                 (self.spawn_default_size[0] * self.size_multiplier,
                                                                  self.spawn_default_size[1] * self.size_multiplier))
                self.end_sprite.image = pygame.transform.scale(self.end_sprite.image,
                                                               (self.end_default_size[0] * self.size_multiplier,
                                                                self.end_default_size[1] * self.size_multiplier))
                self.spawn_sprite.rect = self.spawn_sprite.image.get_rect()
                self.end_sprite.rect = self.end_sprite.image.get_rect()

                self.spawn_sprite.rect.midbottom = (self.level.spawn[0] * self.grid.cell_size,
                                                    self.level.spawn[1] * self.grid.cell_size)
                self.end_sprite.rect.midbottom = (self.level.end[0] * self.grid.cell_size,
                                                  self.level.end[1] * self.grid.cell_size)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.current_button and self.current_button.count >= 1:
                changer = MellingChanger(self, self.current_button.changer_img, self.current_button.melling_class,
                                         m=self.size_multiplier)
                changer.rect.center = (pygame.mouse.get_pos()[0] - self.layers["game"][1][0],
                                       pygame.mouse.get_pos()[1] - self.layers["game"][1][1])
                self.melling_changers.append(changer)
                self.current_button.count -= 1

    def draw_buttons(self):
        # Добавление кнопок персонажей
        buttons_title = ["basher", "blocker", "bomber", "builder", "climber", "digger", "floater", "miner"]
        buttons_class = [Basher, Blocker, Bomber, Builder, Climber, Digger, Floater, Miner]
        self.buttons = [
            LemmingButton(self, f"buttons\\{buttons_title[i]}.jpg", buttons_class[i], (i * 32, self.game.size[1] - 40),
                          self.change_selected, self.level.buttons_count[i], arg=i) for i in range(len(buttons_title))]

        self.boom_button = Button(self, "buttons\\bomb.jpg", (8 * 32, self.game.size[1] - 40),
                                  lambda: [change_character(i, Bomber, -1) for i in self.players_group.sprites()])

    def change_selected(self, game: MainWindow, index: int):
        # Изменение нажатой кнопки
        b = self.buttons[index].activated
        for i in self.buttons:
            i.set_activated(False)
        self.buttons[index].set_activated(not b)
        if not b:
            self.current_button = self.buttons[index]
        else:
            self.current_button = None

    def is_collide(self, sprite):
        # Проверка пересекатеся ли данный спрайт с grid collider или blocker
        collider = self.grid.get_collider()
        return bool(pygame.sprite.collide_mask(sprite, collider) or pygame.sprite.spritecollide(sprite, self.blockers,
                                                                                                dokill=False))
