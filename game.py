import pygame


class Window:
    def __init__(self, title, size):
        self.fps = 60
        pygame.init()
        pygame.display.set_caption(title)
        flags = pygame.SCALED | pygame.FULLSCREEN
        self.surface = pygame.display.set_mode(size, flags=flags, vsync=1)
        self.size = size
        self.clock = pygame.time.Clock()
        from screens.game_screen import GameScreen
        self.screen = GameScreen(self, "level")
        self.start()
        self.screen.start()

        running = True
        while running:
            self.update()
            self.screen.update()
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
            self.event(events)
            self.screen.event(events)
            pygame.display.flip()
            self.clock.tick()

    def update(self):
        pass

    def start(self):
        pass

    def event(self, event):
        pass
