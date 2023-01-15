import pygame


def draw_text(surface: pygame.Surface, position: tuple[int, int], text: str, size: int, color, centered: bool = False):
    font = pygame.font.Font("data\\pixelfont_7.ttf", size)
    text = font.render(text, True, color)
    if centered:
        indent = (surface.get_width() - text.get_width()) // 2
        position = indent, position[1]
    surface.blit(text, position)
