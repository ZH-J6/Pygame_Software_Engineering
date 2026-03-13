import pygame
import math

from setting import WIDTH, HEIGHT, FPS
from player import Player
from weapon import Weapon
from bullet import Bullet
from effects import Explosion, MuzzleFlash, HitSpark
from map import generate_walls


pygame.init()

font = pygame.font.SysFont(None,20)
big_font = pygame.font.SysFont(None,80)

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Tank Battle")

clock = pygame.time.Clock()


weapon = Weapon("Pistol",12,400)


# 两个玩家出生点（对角）
spawn_points = [
(80,80),
(WIDTH-80,HEIGHT-80)
]


players = [

Player(spawn_points[0][0],spawn_points[0][1],(0,255,0),weapon,"P1"),
Player(spawn_points[1][0],spawn_points[1][1],(255,0,0),weapon,"P2")

]


bullets = []
explosions = []
flashes = []
sparks = []

walls = generate_walls()

running = True
winner = None
game_over = False
death_timer = 0


# 玩家移动 + 墙体碰撞
def move_with_collision(player,dx,dy):

    old_x = player.x
    old_y = player.y

    player.move(dx,dy,WIDTH,HEIGHT)

    player_rect = pygame.Rect(player.x-15,player.y-15,30,30)

    for wall in walls:

        if player_rect.colliderect(wall):

            player.x = old_x
            player.y = old_y
            break



while running:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    keys = pygame.key.get_pressed()


    # Player 1
    dx1 = dy1 = 0

    if keys[pygame.K_w]: dy1 = -1
    if keys[pygame.K_s]: dy1 = 1
    if keys[pygame.K_a]: dx1 = -1
    if keys[pygame.K_d]: dx1 = 1


    # Player 2
    dx2 = dy2 = 0

    if keys[pygame.K_UP]: dy2 = -1
    if keys[pygame.K_DOWN]: dy2 = 1
    if keys[pygame.K_LEFT]: dx2 = -1
    if keys[pygame.K_RIGHT]: dx2 = 1


    if not game_over:

        move_with_collision(players[0],dx1,dy1)
        move_with_collision(players[1],dx2,dy2)


    # 射击
    if not game_over and keys[pygame.K_f]:
        players[0].shoot(bullets,flashes)

    if not game_over and keys[pygame.K_l]:
        players[1].shoot(bullets,flashes)



    for bullet in bullets[:]:

        bullet.update()

        if bullet.x < 0 or bullet.x > WIDTH or bullet.y < 0 or bullet.y > HEIGHT:
            bullets.remove(bullet)
            continue


        # 子弹撞墙
        for wall in walls:

            if wall.collidepoint(bullet.x,bullet.y):

                sparks.append(HitSpark(bullet.x,bullet.y))
                bullets.remove(bullet)
                break


        # 子弹击中玩家
        for player in players:

            if bullet.owner == player:
                continue

            dist = math.sqrt((bullet.x-player.x)**2 + (bullet.y-player.y)**2)

            if dist < 15:

                player.hp -= bullet.damage
                sparks.append(HitSpark(bullet.x,bullet.y))

                if player.hp <= 0:

                    player.alive = False
                    explosions.append(
                        Explosion(int(player.x),int(player.y))
                    )

                bullets.remove(bullet)
                break



    alive_players = [p for p in players if p.hp > 0]

    if len(alive_players) == 1 and not game_over:

        winner = alive_players[0].name
        game_over = True
        death_timer = pygame.time.get_ticks()



    screen.fill((0,0,0))


    # 绘制墙
    for wall in walls:
        pygame.draw.rect(screen,(180,80,40),wall)


    # 绘制玩家
    for player in players:
        if player.alive:
            player.draw(screen,font)


    # 子弹
    for bullet in bullets:
        bullet.draw(screen)


    # 特效
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


    if game_over:
        if pygame.time.get_ticks() - death_timer > 1000:
            running = False



if winner:

    screen.fill((10,10,20))

    text = big_font.render(f"{winner} Wins!",True,(255,220,0))
    rect = text.get_rect(center=(WIDTH//2,HEIGHT//2))

    screen.blit(text,rect)

    pygame.display.flip()

    pygame.time.wait(1000)


pygame.quit()