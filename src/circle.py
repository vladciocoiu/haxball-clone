import numpy as np
import pygame as pg

ELASTICITY = 0.3 # amount of velocity that is preserved after a collision between circles

BOUNCINESS = 0.7 # amount of velocity that is preserved after a collision with a wall

EPSILON = 0.02 # minimum velocity before it becomes 0, made for smoother movement

class Circle:
    def __init__(self, mass, pos, r, color, max_speed, outline_thickness, acc, friction_constant):
        self.mass = mass
        self.pos = pos
        self.r = r
        self.color = color
        self.vel = np.array([0.0, 0.0])
        self.MAX_SPEED = max_speed
        self.outline_thickness = outline_thickness
        self.acc = acc
        self.friction_constant = friction_constant

    # draw circle and outline on screen
    def display(self, screen, transparent_surface):
        pg.draw.circle(screen, self.color, self.pos, self.r)
        pg.draw.circle(screen, (0, 0, 0), self.pos, self.r + self.outline_thickness, self.outline_thickness)

    # if 2 circles overlap, we push them apart proportional to their inverse mass
    def penetration_resolution(self, other_circle):
        # vector from other_circle.pos to self.pos
        dist = self.pos - other_circle.pos

        # amount of overlap
        penetration_depth = self.r + other_circle.r + other_circle.outline_thickness - np.linalg.norm(dist)

        # push circles apart 
        penetration_res = dist / np.linalg.norm(dist) * penetration_depth / (self.mass + other_circle.mass)
        self.pos += penetration_res * other_circle.mass
        other_circle.pos -= penetration_res * self.mass
    
    # adjusts velocities after collision
    def collide(self, other_circle):

        # do nothing if the circles don't touch
        if np.linalg.norm(self.pos - other_circle.pos) >= self.r + other_circle.r + other_circle.outline_thickness:
            return

        # resolve penetration firstly
        self.penetration_resolution(other_circle)

        # normalized vector in the direction of self.pos from other_circle.pos
        normal = (self.pos - other_circle.pos) / (np.linalg.norm(self.pos - other_circle.pos))


        vel_diff = self.vel - other_circle.vel

        sep_vel = vel_diff.dot(normal)

        # preserve only a part of the velocities
        new_sep_vel = -sep_vel * ELASTICITY

        sep_vel_diff = new_sep_vel - sep_vel

        # get the vector that we need to add / subtract from the velocities
        adjust_vec = normal * sep_vel_diff / (self.mass + other_circle.mass)

        # update velocities proportional to their inverse masses
        self.vel += adjust_vec * other_circle.mass
        other_circle.vel -= adjust_vec * self.mass

    # invert velocities after the circle touches the wall, preserving only a fraction of the initial velocity
    def bounce(self, width, height):
        if self.pos[0] <= self.r:
            self.pos[0] = self.r
            self.vel[0] *= -BOUNCINESS
        
        if self.pos[1] <= self.r:
            self.pos[1] = self.r
            self.vel[1] *= -BOUNCINESS
                    
        if self.pos[0] >= width - self.r:
            self.pos[0] = width - self.r
            self.vel[0] *= -BOUNCINESS
                    
        if self.pos[1] >= height - self.r:
            self.pos[1] = height - self.r
            self.vel[1] *= -BOUNCINESS
    

    # compute new velocity and position
    def move(self, dir, width, height):

        # add velocity in direction dir
        self.vel += dir * self.acc / self.mass

        # add friction
        self.vel *= self.friction_constant

        # make the velocity 0 when it is smaller than the threshold for a smoother movement
        for idx in range(2):
            if abs(self.vel[idx]) < EPSILON:
                self.vel[idx] = 0;

        # cap magnitude of velocity vector
        vel_mag = np.sqrt(self.vel.dot(self.vel))
        if vel_mag > self.MAX_SPEED:
            self.vel = self.vel * self.MAX_SPEED / vel_mag
         
        # actual movement
        self.pos += self.vel

        # prevent from going out of bounds
        self.pos = np.clip(self.pos, [self.r, self.r], [width - self.r, height - self.r])

