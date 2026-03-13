import pygame
import math

class Bullet:

    def __init__(self,x,y,dir_x,dir_y,damage,owner):

        self.x = x
        self.y = y
        self.damage = damage
        self.owner = owner
        self.speed = 10

        length = math.sqrt(dir_x*dir_x + dir_y*dir_y)

        self.vx = dir_x/length * self.speed
        self.vy = dir_y/length * self.speed

    def update(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self,screen):
        pygame.draw.circle(screen,(255,220,50),(int(self.x),int(self.y)),5)
        pygame.draw.circle(screen,(255,120,0),(int(self.x),int(self.y)),3)