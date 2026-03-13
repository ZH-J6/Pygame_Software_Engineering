import pygame
import math

class Bullet:
    def __init__(self, x, y, target_x, target_y, damage,owner):
        self.x = x
        self.y = y
        self.speed = 8
        self.damage = damage
        self.owner = owner

        dx = target_x - x
        dy = target_y - y
        dist = math.sqrt(dx*dx + dy*dy)

        if dist != 0:
            self.vx = dx/dist * self.speed
            self.vy = dy/dist * self.speed
        else:
            self.vx = 0
            self.vy = 0

    def update(self):
        self.x += self.vx
        self.y += self.vy