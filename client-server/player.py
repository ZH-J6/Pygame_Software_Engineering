import pygame
from bullet import Bullet

class Player:
    def __init__(self,x,y,color,weapon, name):
        self.x = x
        self.y = y
        self.color = color
        self.weapon = weapon
        self.name = name
        self.hp = 100
        self.speed = 4
        self.last_shot = 0
        self.radius = 15

    def move(self,dx,dy):
        self.x += dx*self.speed
        self.y += dy*self.speed

    def shoot(self,target_x,target_y,bullets):
        now = pygame.time.get_ticks()

        if now - self.last_shot > self.weapon.cooldown:
            bullets.append(
                Bullet(self.x,self.y,target_x,target_y,self.weapon.damage,self)
            )
            # print(f"{self.name} schiet! Richting: ({target_x}, {target_y})")
            self.last_shot = now
    
    def take_damage(self, amount):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0

    def draw(self, surface, name_textures):
        # teken speler als cirkel
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

        # teken HP-balk boven speler
        hp_bar_width = 30
        hp_bar_height = 5
        hp_ratio = self.hp / 100  # 0..1
        hp_bar_x = self.x - hp_bar_width / 2
        hp_bar_y = self.y - self.radius - 20
        # achtergrond rood
        pygame.draw.rect(surface, (200,0,0), (hp_bar_x, hp_bar_y, hp_bar_width, hp_bar_height))
        # groen gedeelte
        pygame.draw.rect(surface, (0,200,0), (hp_bar_x, hp_bar_y, hp_bar_width * hp_ratio, hp_bar_height))

        # teken HP-tekst naast de balk
        font = pygame.font.SysFont('Comic Sans MS', 12)
        hp_text = font.render(f"{int(self.hp)}/100", True, (255,255,255))
        surface.blit(hp_text, (hp_bar_x + hp_bar_width + 5, hp_bar_y - 3))  # rechts naast de balk

        # teken naam boven speler
        name_texture = name_textures.get_texture(self.name)
        text_offset = pygame.Vector2(name_texture.get_size())
        text_offset.x /= 2
        text_offset.y += self.radius
        surface.blit(name_texture, (self.x - text_offset.x, self.y - text_offset.y))