import pygame


class Label(pygame.sprite.Sprite):
    containers = ()

    def __init__(self, font: pygame.font.Font, content: str, color: tuple[int, int, int], position: tuple[int, int]):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.font = font
        self.content = content
        self.color = color
        self.position = position

    def draw(self, screen):
        label_surface = self.font.render(self.content, True, self.color)
        screen.blit(label_surface, self.position)
