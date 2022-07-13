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

clock = pg.time.Clock()
while running:
    clock.tick(60)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    keys_pressed = pg.key.get_pressed()

    # send relevant inputs to server
    circles = [p, players, ball] = net.send({
        'x': keys_pressed[pg.K_x],
        'up': keys_pressed[pg.K_UP],
        'down': keys_pressed[pg.K_DOWN],
        'left': keys_pressed[pg.K_LEFT],
        'right': keys_pressed[pg.K_RIGHT],
    })

    screen.fill((70, 150, 70))

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
