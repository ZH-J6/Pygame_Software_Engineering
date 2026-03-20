"""
Visual effects for Tank Battle.

Contains:
- Explosion: particle-based explosion effect for destroyed players.
- MuzzleFlash: brief flash when a bullet is fired.
- HitSpark: small sparks when bullets hit walls or players.

Each effect handles its own update and draw methods.
"""

import pygame
import random
import math
from setting import WIDTH, HEIGHT


class Explosion:

    def __init__(self,x,y):
        """
        Initialize an explosion at the given position.

        Args:
            x, y: Center coordinates of the explosion.
        """
        self.particles = []

        for i in range(20):

            angle = random.uniform(0,2*math.pi)
            speed = random.uniform(3,7)

            vx = math.cos(angle)*speed
            vy = math.sin(angle)*speed

            self.particles.append([x,y,vx,vy,5])

    def update(self):
        """Update particle positions and reduce their size over time."""
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
        """Draw the explosion particles on the screen."""
        for p in self.particles:

            color=(255,max(50,int(150*p[4]/5)),0)

            pygame.draw.circle(screen,color,(int(p[0]),int(p[1])),int(p[4]))


class MuzzleFlash:
    """
    Muzzle flash effect for shooting bullets.

    Attributes:
        x, y: Position of the flash.
        life: How many frames the flash lasts.
    """
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.life = 6

    def update(self):
        """Decrease the flash's life each frame."""
        self.life -= 1

    def draw(self,screen):
        """Draw the muzzle flash on the screen."""
        pygame.draw.circle(screen,(255,220,120),(int(self.x),int(self.y)),10)
        pygame.draw.circle(screen,(255,150,0),(int(self.x),int(self.y)),5)


class HitSpark:
    """
    Hit spark effect when bullets collide with walls or players.

    Attributes:
        particles: List of particles, each represented as [x, y, vx, vy, size].
    """
    def __init__(self,x,y):

        self.particles=[]

        for i in range(8):

            angle=random.uniform(0,2*math.pi)
            speed=random.uniform(2,5)

            vx=math.cos(angle)*speed
            vy=math.sin(angle)*speed

            self.particles.append([x,y,vx,vy,4])

    def update(self):
        """Update spark particle positions and reduce their size over time."""
        for p in self.particles:

            p[0]+=p[2]
            p[1]+=p[3]

            p[4]-=0.2

        self.particles=[p for p in self.particles if p[4]>0]

    def draw(self,screen):
        """Draw the hit sparks on the screen."""
        for p in self.particles:

            pygame.draw.circle(screen,(255,220,50),(int(p[0]),int(p[1])),int(p[4]))