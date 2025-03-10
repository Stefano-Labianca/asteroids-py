import sys

import pygame

from common.constants import *
from entity.asteroid import Asteroid
from entity.particle import Particle
from entity.player import Player
from entity.shot import Shot
from ui.label import Label
from utility.asteroidfield import AsteroidField
from utility.events import ASTEROID_DESTROYED, PLAYER_DEAD, PLAYER_RESPAWN


def main():
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    shots = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()

    Particle.containers = (drawable, updatable)
    Label.containers = (drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = (updatable)
    Asteroid.containers = (asteroids, updatable, drawable)
    Player.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 3)
    asteroid_field = AsteroidField()

    font = pygame.font.Font(None, 24)
    score_surface = Label(font, "SCORE: 0", (255, 255, 255), (10, 10))
    lives_surface = Label(
        font, f"LIVES: {player.lives}", (255, 255, 255), (10, 30)
    )

    respawn = 1.5 * 1000
    score = 0
    dt = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == ASTEROID_DESTROYED:
                score += event.dict["points"]

                score_surface.kill()
                score_surface = Label(
                    font, f"SCORE: {score}", (255, 255, 255), (10, 10)
                )

            if event.type == PLAYER_DEAD:
                pygame.time.set_timer(PLAYER_RESPAWN, int(respawn))

            if event.type == PLAYER_RESPAWN:
                pygame.time.set_timer(PLAYER_RESPAWN, 0)
                player = Player(
                    SCREEN_WIDTH / 2,
                    SCREEN_HEIGHT / 2,
                    player.lives
                )

        updatable.update(dt)

        for asteroid in asteroids:
            if player.lives == 0:
                print("Game Over!")
                sys.exit()

            if asteroid.check_collision(player) and player.alive():
                player.kill()
                lives_surface.kill()

                player.lives -= 1
                lives_surface = Label(
                    font, f"LIVES: {player.lives}", (255, 255, 255), (10, 30)
                )

                pygame.event.post(
                    pygame.event.Event(PLAYER_DEAD)
                )

            for shot in shots:
                if asteroid.check_collision(shot):
                    shot.kill()
                    asteroid.draw_explosion_effect()
                    asteroid.split()

        screen.fill((0, 0, 0))

        for obj in drawable:
            obj.draw(screen)

        pygame.display.flip()

        # Limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
