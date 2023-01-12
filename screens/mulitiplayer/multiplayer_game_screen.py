from screens.change_screen import change_screen
from screens.game_screen import GameScreen
from screens.mulitiplayer.winner_screen import WinnerScreen
from ui.text import draw_text


class MultiplayerGameScreen(GameScreen):
    def __init__(self, game, level, sock, thread=None):
        super().__init__(game, level)
        self.thread = thread
        self.sock = sock
        self.other_completed = None

    def custom_update(self):
        send = f"У противника завершило: {self.characters_complete}"

        if self.spawn_count == 0:
            if self.thread:
                if self.other_completed is not None:
                    if self.characters_complete > self.other_completed:
                        send = "winner 0"
                    elif self.characters_complete == self.other_completed:
                        send = "winner 1"
                    elif self.characters_complete < self.other_completed:
                        send = "winner 2"
                    winner_title = {"0": "Вы победили", "1": "Ничья", "2": "Вы проиграли"}
                    change_screen(self.game, WinnerScreen(self.game, winner_title[send.split()[1]]))
            else:
                send = f"completed {self.characters_complete}"

        if self.thread:
            self.sock.send(send.encode())
        data = self.sock.recv(1024).decode()

        if data.startswith("completed"):
            self.other_completed = int(data.split()[1])
        elif data.startswith("winner"):
            winner_title = {"0": "Вы проиграли", "1": "Ничья", "2": "Вы победили"}
            change_screen(self.game, WinnerScreen(self.game, winner_title[data.split()[1]]))
        if not self.thread:
            self.sock.send(send.encode())
        draw_text(self.layers["gui"][0], (20, 20), data, 20, "black", centered=True)
