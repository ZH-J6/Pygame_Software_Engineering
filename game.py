import pygame
import random
import math


pygame.init()

font = pygame.font.SysFont(None, 36)

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2 Player Shooter")

clock = pygame.time.Clock()


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


class Bullet:
    def __init__(self, x, y, dir_x, dir_y, damage, owner):

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

    def draw(self):
        pygame.draw.circle(screen,(255,255,0),(int(self.x),int(self.y)),4)


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

    def move(self,dx,dy):
        if dx != 0 or dy != 0:
            self.dir_x = dx
            self.dir_y = dy

            self.x += dx*self.speed
            self.y += dy*self.speed

            self.x = max(0,min(WIDTH,self.x))
            self.y = max(0,min(HEIGHT,self.y))

    def shoot(self,target_x,target_y,bullets):
        now = pygame.time.get_ticks()

        if now - self.last_shot > self.weapon.cooldown:
            bullets.append(
                Bullet(self.x,self.y,self.dir_x,self.dir_y,self.weapon.damage,self)
            )
            self.last_shot = now

    def draw(self):
        pygame.draw.circle(screen,self.color,(int(self.x),int(self.y)),15)
        name_text = font.render(self.name, True, (255,255,255))
        screen.blit(name_text,(self.x-20,self.y-35))

def draw_hp(player, x, y):

    text = font.render(f"HP: {player.hp}", True, (255,255,255))
    screen.blit(text, (x,y))

    bar_width = 200
    bar_height = 20

    pygame.draw.rect(screen,(100,0,0),(x,y+30,bar_width,bar_height))
    pygame.draw.rect(screen,(0,255,0),(x,y+30,player.hp*2,bar_height))


# 随机武器
player1_weapon = random.choice(weapons)
player2_weapon = random.choice(weapons)

print("Player1 weapon:",player1_weapon.name)
print("Player2 weapon:",player2_weapon.name)

player1 = Player(200,300,(0,255,0),player1_weapon,"Player 1")
player2 = Player(600,300,(255,0,0),player2_weapon,"Player 2")

bullets = []

running = True
winner = None

while running:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Player1 movement
    dx1 = dy1 = 0
    if keys[pygame.K_w]:
        dy1 = -1
    if keys[pygame.K_s]:
        dy1 = 1
    if keys[pygame.K_a]:
        dx1 = -1
    if keys[pygame.K_d]:
        dx1 = 1

    player1.move(dx1,dy1)

    # Player2 movement
    dx2 = dy2 = 0
    if keys[pygame.K_UP]:
        dy2 = -1
    if keys[pygame.K_DOWN]:
        dy2 = 1
    if keys[pygame.K_LEFT]:
        dx2 = -1
    if keys[pygame.K_RIGHT]:
        dx2 = 1

    player2.move(dx2,dy2)

    # Player1 shoot (F)
    if keys[pygame.K_f]:
        player1.shoot(player2.x,player2.y,bullets)

    # Player2 shoot (L)
    if keys[pygame.K_l]:
        player2.shoot(player1.x,player1.y,bullets)

    # 更新子弹
    for bullet in bullets[:]:
        bullet.update()
        if bullet.x < 0 or bullet.x > WIDTH or bullet.y < 0 or bullet.y > HEIGHT:
            bullets.remove(bullet)
            continue

        dist1 = math.sqrt((bullet.x-player1.x)**2+(bullet.y-player1.y)**2)
        dist2 = math.sqrt((bullet.x-player2.x)**2+(bullet.y-player2.y)**2)

        if dist1 < 15 and bullet.owner != player1:
            player1.hp -= bullet.damage
            bullets.remove(bullet)

        elif dist2 < 15 and bullet.owner != player2:
            player2.hp -= bullet.damage
            bullets.remove(bullet)

    # 胜负判定
    if player1.hp <= 0:
        winner = "Player 2 Wins!"
        running = False

    if player2.hp <= 0:
        winner = "Player 1 Wins!"
        running = False

    screen.fill((30,30,30))

    player1.draw()
    player2.draw()

    draw_hp(player1, 20, 20)
    draw_hp(player2, WIDTH-220, 20)

    for bullet in bullets:
        bullet.draw()

    pygame.display.flip()


pygame.quit()

if winner:
    print(winner)