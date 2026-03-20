"""
Bullet system for Tank Battle.

Defines the Bullet class which handles:
- Position, speed, and direction of travel.
- Updating the bullet's position each frame.
- Drawing bullets on the screen with a simple visual effect.
- Tracking ownership and damage value.
"""

import pygame
import math

class Bullet:
    """
    Bullet class representing a projectile fired by a player.

    Attributes:
        x, y: Current position of the bullet.
        vx, vy: Velocity components based on direction and speed.
        damage: Damage dealt to a player on hit.
        owner: Reference to the Player who fired the bullet.
        speed: Movement speed of the bullet.
    """

    def __init__(self,x,y,dir_x,dir_y,damage,owner):
        """
        Initialize a bullet.

        Args:
            x, y: Spawn position.
            dir_x, dir_y: Direction vector.
            damage: Damage value of the bullet.
            owner: Player object who fired the bullet.
        """
        self.x = x
        self.y = y
        self.damage = damage
        self.owner = owner
        self.speed = 10

        length = math.sqrt(dir_x*dir_x + dir_y*dir_y)

        self.vx = dir_x/length * self.speed
        self.vy = dir_y/length * self.speed

    def update(self):
        """Update the bullet's position."""
        self.x += self.vx
        self.y += self.vy

    def draw(self,screen):
        """Draw the bullet on the screen."""
        pygame.draw.circle(screen,(255,220,50),(int(self.x),int(self.y)),5)
        pygame.draw.circle(screen,(255,120,0),(int(self.x),int(self.y)),3)