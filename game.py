import pygame


class Window:
    def __init__(self, title, size):
        pygame.init()
        pygame.display.set_caption(title)
        flags = pygame.SCALED # | pygame.FULLSCREEN
        self.screen = pygame.display.set_mode(size, flags, vsync=1)
        self.size = size
        self.clock = pygame.time.Clock()
        self.start()

        running = True
        while running:
            self.update()
            for event in pygame.event.get():
                self.event(event)
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.flip()
            self.clock.tick()

    def update(self):
        pass

    def start(self):
        pass

    def event(self, event):
        pass
