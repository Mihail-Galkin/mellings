import pygame


class Window:
    def __init__(self, title, size):
        self.fps = 500
        pygame.init()
        pygame.display.set_caption(title)
        # flags = pygame.SCALED | pygame.FULLSCREEN
        self.surface = pygame.display.set_mode(size)
        self.size = size
        self.clock = pygame.time.Clock()
        from screens.main_menu_screen import MainMenuScreen
        self.screen = MainMenuScreen(self)
        self.start()
        self.screen.start()

        running = True
        while running:
            self.surface.fill("black")
            self.update()
            self.screen.update()
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                    self.close()
            self.event(events)
            self.screen.event(events)

            for i in list(self.screen.layers.values())[::-1]:
                self.surface.blit(*i)

            pygame.display.flip()

            self.clock.tick(100)

    def update(self):
        pass

    def start(self):
        pass

    def event(self, event):
        pass

    def close(self):
        pass
