import pygame as pg
import numpy as np

from circle import Circle
from player import Player

pg.init()

size = width, height = 800, 600

screen = pg.display.set_mode(size)

transparent_surface = pg.Surface((width, height), pg.SRCALPHA)

circles = [player, ball] = [
    Player(8, np.array([width / 2 - 50, height / 2]), 25, (200, 30, 30), 1.5, 2, 0.3, 0.98, 3.3),
    Circle(1, np.array([width / 2, height / 2]), 15, (255, 255, 255), 30, 2, 0, 0.99)
]

# main game loop
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        # update shooting state of player
        if event.type == pg.KEYDOWN and event.key == pg.K_x:
            player.changeShootingState(True)
        
        if event.type == pg.KEYUP and event.key == pg.K_x:
            player.changeShootingState(False)

    screen.fill((30, 200, 30))

    # get direction of player movement based on keys pressed
    keys_pressed = pg.key.get_pressed()
    dir = np.array([
        np.float64(keys_pressed[pg.K_RIGHT] - keys_pressed[pg.K_LEFT]),
        np.float64(keys_pressed[pg.K_DOWN] - keys_pressed[pg.K_UP])
    ])

    # resolve collisions
    for i in range(len(circles)):
        for j in range(i + 1, len(circles)):
            circles[i].collide(circles[j])

    # remove shooting state if the player already shot the ball
    if player.shoot(ball):
        player.changeShootingState(False)

    # move, display and bounce for every circle
    ball.move(np.zeros(2), width, height)
    player.move(np.array(dir), width, height)
    for circle in circles:
        circle.display(screen, transparent_surface)
        circle.bounce(width, height)

    pg.display.flip()

pg.quit()
