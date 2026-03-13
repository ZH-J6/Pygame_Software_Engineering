import pygame
import random
import math
from setting import WIDTH, HEIGHT


class Explosion:

    def __init__(self,x,y):

        self.particles = []

        for i in range(20):

            angle = random.uniform(0,2*math.pi)
            speed = random.uniform(3,7)

            vx = math.cos(angle)*speed
            vy = math.sin(angle)*speed

            self.particles.append([x,y,vx,vy,5])

    def update(self):

        for p in self.particles:

            p[0]+=p[2]
            p[1]+=p[3]

            p[4]-=0.1

            if p[0]<0 or p[0]>WIDTH:
                p[2]*=-1

            if p[1]<0 or p[1]>HEIGHT:
                p[3]*=-1

        self.particles=[p for p in self.particles if p[4]>0]

    def draw(self,screen):

        for p in self.particles:

            color=(255,max(50,int(150*p[4]/5)),0)

            pygame.draw.circle(screen,color,(int(p[0]),int(p[1])),int(p[4]))


class MuzzleFlash:

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.life = 6

    def update(self):
        self.life -= 1

    def draw(self,screen):

        pygame.draw.circle(screen,(255,220,120),(int(self.x),int(self.y)),10)
        pygame.draw.circle(screen,(255,150,0),(int(self.x),int(self.y)),5)


class HitSpark:

    def __init__(self,x,y):

        self.particles=[]

        for i in range(8):

            angle=random.uniform(0,2*math.pi)
            speed=random.uniform(2,5)

            vx=math.cos(angle)*speed
            vy=math.sin(angle)*speed

            self.particles.append([x,y,vx,vy,4])

    def update(self):

        for p in self.particles:

            p[0]+=p[2]
            p[1]+=p[3]

            p[4]-=0.2

        self.particles=[p for p in self.particles if p[4]>0]

    def draw(self,screen):

        for p in self.particles:

            pygame.draw.circle(screen,(255,220,50),(int(p[0]),int(p[1])),int(p[4]))