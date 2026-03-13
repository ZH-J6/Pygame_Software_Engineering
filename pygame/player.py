import pygame
from bullet import Bullet


class Player:

    def __init__(self,x,y,color,weapon,name):

        self.x = x
        self.y = y
        self.color = color
        self.weapon = weapon
        self.hp = 100
        self.speed = 4
        self.last_shot = 0
        self.dir_x = 1
        self.dir_y = 0
        self.name = name
        self.alive = True

    def move(self,dx,dy,width,height):

        if dx!=0 or dy!=0:
            self.dir_x = dx
            self.dir_y = dy

        self.x += dx*self.speed
        self.y += dy*self.speed

        self.x=max(0,min(width,self.x))
        self.y=max(0,min(height,self.y))

    def shoot(self,bullets,flashes):

        now = pygame.time.get_ticks()

        if now-self.last_shot > self.weapon.cooldown:

            bullets.append(
                Bullet(self.x,self.y,self.dir_x,self.dir_y,self.weapon.damage,self)
            )

            from effects import MuzzleFlash
            flashes.append(MuzzleFlash(self.x,self.y))

            self.last_shot = now

    def draw(self,screen,font):

        if not self.alive:
            return

        x = int(self.x)
        y = int(self.y)

        pygame.draw.circle(screen,self.color,(x,y),15)

        # 玩家名字
        name_text = font.render(self.name,True,(255,255,255))
        name_rect = name_text.get_rect(center=(x,y-35))
        screen.blit(name_text,name_rect)

        # 血条
        hp = max(0,self.hp)

        bar_width = 40
        bar_height = 6

        bar_x = x - bar_width//2
        bar_y = y - 50

        pygame.draw.rect(screen,(100,0,0),(bar_x,bar_y,bar_width,bar_height))
        pygame.draw.rect(screen,(0,255,0),(bar_x,bar_y,bar_width*(hp/100),bar_height))