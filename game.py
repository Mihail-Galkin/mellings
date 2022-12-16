import pygame


class Window:
    def __init__(self, title, size, fps):
        pygame.init()
        pygame.display.set_caption(title)
        self.screen = pygame.display.set_mode(size)
        self.size = size
        self.clock = pygame.time.Clock()
        self.start()
        self.fps = fps

        running = True
        while running:
            self.update()
            for event in pygame.event.get():
                self.event(event)
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.flip()
            self.clock.tick(self.fps)

    def update(self):
        pass

    def start(self):
        pass

    def event(self, event):
        pass
