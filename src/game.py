import pygame as pg
import numpy as np

from circle import Circle
from player import Player
from network import Network

pg.init()

size = width, height = 800, 600

screen = pg.display.set_mode(size)

transparent_surface = pg.Surface((width, height), pg.SRCALPHA)

# main game loop
running = True
net = Network()
list = [p, circles] = [p, [players, ball]] = net.get_p()

while running:
    circles = [p, players, ball] = net.send(p)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill((70, 150, 70))

    p.move(width, height)
    p.update_shooting_state(ball)

    p.display(screen, transparent_surface)
    for circle in players + [ball]:
        circle.display(screen, transparent_surface)


    # # resolve collisions
    # for i in range(len(players)):
    #     for j in range(i + 1, len(players)):
    #         players[i].collide(players[j])
    #     players[i].collide(ball)

    # # update circles
    # for player in players:
    #     player.update_shooting_state(ball)
    #     player.move(width, height)

    # ball.update(np.zeros(2), width, height)

    # # display and bounce circles
    # for circle in [ball] + players:
    #     circle.display(screen, transparent_surface)
    #     circle.bounce(width, height)

    pg.display.flip()

pg.quit()
