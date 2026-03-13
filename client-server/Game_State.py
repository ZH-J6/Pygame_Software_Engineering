import pygame
from player import Player
from bullet import Bullet

class Game_State:

    def __init__(self, world_size):
        self.world_size = world_size
        self.players = {}
        self.bullets = []

    def update_player(self,action):
        name = action.get_name()
        dx, dy, shoot = action.get_dx(), action.get_dy(), action.get_shoot()

        if name not in self.players:
            from player import Player
            from random import choice
            from weapon import weapons
            weapon = choice(weapons)
            self.players[name] = Player(self.world_size.x//2, self.world_size.y//2, (255,255,255), weapon, name)

        player = self.players[name]
        player.move(dx,dy)
        if shoot:
            player.shoot(shoot[0], shoot[1], self.bullets)

        # Check bullets die deze player raken
        for bullet in self.bullets:
            if bullet.owner != player:
                dist = ((bullet.x - player.x) ** 2 + (bullet.y - player.y) ** 2) ** 0.5
                if dist <= player.radius:
                    player.hp -= bullet.damage
                    if player.hp < 0:
                        player.hp = 0
                    self.bullets.remove(bullet)

        # verwijder speler als HP 0
        if player.hp <= 0:
            del self.players[name]

    def update_bullets(self):
        for bullet in self.bullets[:]:  # kopie om veilig te verwijderen
            bullet.update()
            # verwijder bullet als die buiten het scherm is
            if bullet.x < 0 or bullet.x > self.world_size.x or bullet.y < 0 or bullet.y > self.world_size.y:
                self.bullets.remove(bullet)

    def check_bullet_hits(self):
        for bullet in self.bullets[:]:
            for player in self.players.values():
                if player == bullet.owner:
                    continue  # speler schiet zichzelf niet
                dist = ((player.x - bullet.x)**2 + (player.y - bullet.y)**2)**0.5
                if dist < player.radius:
                    player.take_damage(bullet.damage)
                    self.bullets.remove(bullet)
                    break

    def spawn_units(self):
        pass

    def draw(self, name, surface, name_textures):
        rect = pygame.Rect(0, 0, self.world_size.x, self.world_size.y)
        pygame.draw.rect(surface, (30,30,30), rect)
        for player in self.players.values():
            player.draw(surface, name_textures)
        for bullet in self.bullets:
            pygame.draw.circle(surface, (255, 255, 0), (int(bullet.x), int(bullet.y)), 4)