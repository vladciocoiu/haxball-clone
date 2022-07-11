import numpy as np
import pygame as pg

from circle import Circle

SHOT_RANGE = 5 # max distance between player and ball in order to be able to shoot

class Player(Circle):
    shooting = False

    def __init__(self, mass, pos, r, color, max_speed, outline_thickness, acc, friction_constant, shooting_power):
        super().__init__(mass, pos, r, color, max_speed, outline_thickness, acc, friction_constant)
        self.shooting_power = shooting_power
        self.just_shot = False

    # compute movement direction based on keys pressed and update
    def move(self, width, height):
        keys_pressed = pg.key.get_pressed()
        dir = np.array([
            np.float64(keys_pressed[pg.K_RIGHT] - keys_pressed[pg.K_LEFT]),
            np.float64(keys_pressed[pg.K_DOWN] - keys_pressed[pg.K_UP])
        ])

        self.update(np.array(dir), width, height)

    def display(self, screen, transparent_surface):
        # draw circle
        pg.draw.circle(screen, self.color, self.pos, self.r)

        # draw outline based on shooting state
        pg.draw.circle(screen, np.array((255, 255, 255)) * self.shooting, self.pos, self.r + self.outline_thickness, self.outline_thickness)
        
        # draw semi-transparent circle around the player
        pg.draw.circle(transparent_surface, np.array((255, 255, 255, 75)), self.pos, self.r + 18, 5)
        screen.blit(transparent_surface, (0, 0))
        transparent_surface.fill((0,0,0,0))

    def update_shooting_state(self, ball):

        # change shooting based on keys pressed
        keys_pressed = pg.key.get_pressed()

        if keys_pressed[pg.K_x] and not self.just_shot:
            self.shooting = True
        elif not keys_pressed[pg.K_x]:
            self.just_shot = False
            self.shooting = False

        # remove shooting state if the player already shot the ball
        if self.shoot(ball):
            self.just_shot = True
            self.shooting = False


    def shoot(self, ball):
        if not self.shooting or np.linalg.norm(self.pos - ball.pos) - (self.r + ball.r + ball.outline_thickness) > SHOT_RANGE:
            return False
        
        # normalized vector pointing to ball from self
        dir = (ball.pos - self.pos) / np.linalg.norm(ball.pos - self.pos)

        # add velocity to the ball
        ball.vel += dir * self.shooting_power

        return True