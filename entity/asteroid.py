import math
import random

import pygame

from common.constants import ASTEROID_KINDS, ASTEROID_MIN_RADIUS
from utility.circleshape import CircleShape
from utility.events import ASTEROID_DESTROYED


class Asteroid(CircleShape):
    containers = ()

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255),
                           self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()
        points = int(
            (ASTEROID_KINDS / (self.radius / ASTEROID_MIN_RADIUS)) * 10
        )

        pygame.event.post(
            pygame.event.Event(
                ASTEROID_DESTROYED, {"points": points}
            )
        )

        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        random_angle = random.uniform(20, 50)

        first_velocity_vector = self.velocity.rotate(random_angle) * 1.2
        second_velocity_vector = self.velocity.rotate(-random_angle) * 1.2

        new_radius = self.radius - ASTEROID_MIN_RADIUS

        first_asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        first_asteroid.velocity = first_velocity_vector

        second_asteroid = Asteroid(
            self.position.x, self.position.y, new_radius)
        second_asteroid.velocity = second_velocity_vector
