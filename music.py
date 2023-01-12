from os import listdir
from os.path import isfile, join
import random

import pygame

from main import MainWindow


class MusicManager:
    """
    Класс, реализуующий фоновую музыку
    """
    def __init__(self, game: MainWindow, playlist_path: str):
        self.MUSIC_END = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(self.MUSIC_END)

        self.game = game

        self.playlist = [join(playlist_path, f) for f in listdir(playlist_path) if isfile(join(playlist_path, f))]

        pygame.mixer.music.load(random.choice(self.playlist))
        self.load_music()

        pygame.mixer.music.play(0)

        self.current_volume = game.config.getfloat("GENERAL", "volume")
        pygame.mixer.music.set_volume(self.current_volume)

    def load_music(self) -> None:
        """
        Добавление случайного трека в очередь
        """
        pygame.mixer.music.queue(random.choice(self.playlist))

    def add_volume(self, d: int):
        """
        Добавление громкости
        """
        self.current_volume += d
        if self.current_volume > 1:
            self.current_volume = 1
        elif self.current_volume < 0:
            self.current_volume = 0

        pygame.mixer.music.set_volume(self.current_volume)
        self.game.config.set("GENERAL", "volume", str(self.current_volume))
