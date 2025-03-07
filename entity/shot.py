import pygame

from common.constants import SHOT_RADIUS
from utility.circleshape import CircleShape


class Shot(CircleShape):
    containers = ()

    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)
        self.__time_to_live = 0.7

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255),
                           self.position, self.radius, 2)

    def update(self, dt):
        self.__time_to_live -= dt

        if self.__time_to_live <= 0:
            self.kill()

        self.position += self.velocity * dt
