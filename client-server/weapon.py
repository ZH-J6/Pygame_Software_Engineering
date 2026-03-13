class Weapon:
    def __init__(self, name, damage, cooldown):
        self.name = name
        self.damage = damage
        self.cooldown = cooldown


weapons = [
    Weapon("Pistol", 12, 400),
    Weapon("Rifle", 8, 150),
    Weapon("Sniper", 40, 900)
]