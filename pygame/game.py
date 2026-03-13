import pygame
import random
import math

from setting import WIDTH, HEIGHT, FPS
from player import Player
from weapon import Weapon
from bullet import Bullet
from effects import Explosion, MuzzleFlash, HitSpark
from ui import draw_hp


pygame.init()
pygame.mixer.music.load("bgm.mp3")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)

font = pygame.font.SysFont(None,36)
big_font = pygame.font.SysFont(None,80)

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("2 Player Shooter")

clock = pygame.time.Clock()


weapons = [
    Weapon("Pistol",12,400),
    Weapon("Rifle",8,150),
    Weapon("Sniper",40,900)
]


player1_weapon = random.choice(weapons)
player2_weapon = random.choice(weapons)

player1 = Player(200,300,(0,255,0),player1_weapon,"Player 1")
player2 = Player(600,300,(255,0,0),player2_weapon,"Player 2")


bullets = []
explosions = []
flashes = []
sparks = []

shake = 0

running = True
winner = None
game_over = False
death_timer = 0


while running:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    keys = pygame.key.get_pressed()

    dx1 = dy1 = 0
    dx2 = dy2 = 0

    if keys[pygame.K_w]: dy1 = -1
    if keys[pygame.K_s]: dy1 = 1
    if keys[pygame.K_a]: dx1 = -1
    if keys[pygame.K_d]: dx1 = 1

    if keys[pygame.K_UP]: dy2 = -1
    if keys[pygame.K_DOWN]: dy2 = 1
    if keys[pygame.K_LEFT]: dx2 = -1
    if keys[pygame.K_RIGHT]: dx2 = 1


    if not game_over:
        player1.move(dx1,dy1,WIDTH,HEIGHT)
        player2.move(dx2,dy2,WIDTH,HEIGHT)


    if not game_over and keys[pygame.K_f]:
        player1.shoot(bullets,flashes)

    if not game_over and keys[pygame.K_l]:
        player2.shoot(bullets,flashes)


    for bullet in bullets[:]:

        bullet.update()

        if bullet.x < 0 or bullet.x > WIDTH or bullet.y < 0 or bullet.y > HEIGHT:
            bullets.remove(bullet)
            continue


        dist1 = math.sqrt((bullet.x-player1.x)**2 + (bullet.y-player1.y)**2)
        dist2 = math.sqrt((bullet.x-player2.x)**2 + (bullet.y-player2.y)**2)


        if dist1 < 15 and bullet.owner != player1:

            player1.hp -= bullet.damage
            sparks.append(HitSpark(bullet.x,bullet.y))
            shake = 10
            bullets.remove(bullet)

        elif dist2 < 15 and bullet.owner != player2:

            player2.hp -= bullet.damage
            sparks.append(HitSpark(bullet.x,bullet.y))
            shake = 10
            bullets.remove(bullet)


    if player1.hp <= 0 and not game_over:

        player1.alive = False
        explosions.append(Explosion(int(player1.x),int(player1.y)))
        shake = 20
        winner = "Player 2 Wins!"
        game_over = True
        death_timer = pygame.time.get_ticks()


    if player2.hp <= 0 and not game_over:

        player2.alive = False
        explosions.append(Explosion(int(player2.x),int(player2.y)))
        shake = 20
        winner = "Player 1 Wins!"
        game_over = True
        death_timer = pygame.time.get_ticks()


    offset_x = random.randint(-shake,shake)
    offset_y = random.randint(-shake,shake)


    for x in range(0,WIDTH,40):
        for y in range(0,HEIGHT,40):

            color = (20,20,40)

            if (x+y)//40 % 2 == 0:
                color = (30,30,60)

            pygame.draw.rect(screen,color,(x+offset_x,y+offset_y,40,40))


    player1.draw(screen,font)
    player2.draw(screen,font)

    draw_hp(player1,20,20,screen,font)
    draw_hp(player2,WIDTH-220,20,screen,font)


    for bullet in bullets:
        bullet.draw(screen)


    for e in explosions[:]:

        e.update()
        e.draw(screen)

        if len(e.particles) == 0:
            explosions.remove(e)


    for f in flashes[:]:

        f.update()
        f.draw(screen)

        if f.life <= 0:
            flashes.remove(f)


    for s in sparks[:]:

        s.update()
        s.draw(screen)

        if len(s.particles) == 0:
            sparks.remove(s)


    pygame.display.flip()

    shake = max(0,shake-1)


    if game_over:
        if pygame.time.get_ticks() - death_timer > 1000:
            running = False



if winner:

    screen.fill((10,10,20))

    text = big_font.render(winner,True,(255,220,0))
    rect = text.get_rect(center=(WIDTH//2,HEIGHT//2))

    screen.blit(text,rect)

    pygame.display.flip()

    pygame.time.wait(1000)


pygame.quit()