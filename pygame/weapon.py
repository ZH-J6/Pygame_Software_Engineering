"""
Weapon system for Tank Battle.

Defines the Weapon class which stores:
- Name of the weapon.
- Damage dealt by bullets.
- Cooldown time between shots.
"""

class Weapon:
    def __init__(self,name,damage,cooldown):
        self.name = name
        self.damage = damage
        self.cooldown = cooldown
