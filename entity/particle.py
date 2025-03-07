import pygame

from utility.squareshape import SquareShape


class Particle(SquareShape):
    containers = ()

    def __init__(self, x: int, y: int, w: int, h: int):
        super().__init__(x, y, w, h)
        self.__time_to_live = 0.23

    def draw(self, screen):
        pygame.draw.rect(
            screen, (255, 255, 255),
            (self.position.x, self.position.y, self.w, self.h), 1
        )

    def update(self, dt):
        self.__time_to_live -= dt

        if self.__time_to_live <= 0:
            self.kill()

        self.position += self.velocity * dt
