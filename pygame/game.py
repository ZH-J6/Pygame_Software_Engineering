import pygame
import math

from setting import WIDTH, HEIGHT, FPS
from player import Player
from weapon import Weapon
from bullet import Bullet
from effects import Explosion, MuzzleFlash, HitSpark
from map import generate_walls


pygame.init()
pygame.mixer.music.load("assets/bgm.mp3")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)

font = pygame.font.SysFont(None,20)
big_font = pygame.font.SysFont(None,80)

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Tank Battle")

clock = pygame.time.Clock()

weapon = Weapon("Missile",12,400)


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


def move_with_collision(player,dx,dy):

    old_x = player.x
    old_y = player.y

    player.move(dx,dy,WIDTH,HEIGHT)

    rect = pygame.Rect(player.x-20,player.y-20,40,40)

    for wall in walls:

        if rect.colliderect(wall):

            player.x = old_x
            player.y = old_y
            break


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

        move_with_collision(players[0],dx1,dy1)
        move_with_collision(players[1],dx2,dy2)


    if not game_over and keys[pygame.K_f]:

        spawn_x = players[0].x + players[0].dir_x * 25
        spawn_y = players[0].y + players[0].dir_y * 25

        players[0].shoot(bullets,flashes,spawn_x,spawn_y)


    if not game_over and keys[pygame.K_l]:

        spawn_x = players[1].x + players[1].dir_x * 25
        spawn_y = players[1].y + players[1].dir_y * 25

        players[1].shoot(bullets,flashes,spawn_x,spawn_y)



    for bullet in bullets[:]:

        bullet.update()

        if bullet.x < 0 or bullet.x > WIDTH or bullet.y < 0 or bullet.y > HEIGHT:
            bullets.remove(bullet)
            continue


        hit_wall = False

        for wall in walls:

            if wall.collidepoint(bullet.x,bullet.y):

                sparks.append(HitSpark(bullet.x,bullet.y))
                bullets.remove(bullet)
                hit_wall = True
                break

        if hit_wall:
            continue


        for player in players:

            if bullet.owner == player:
                continue

            dist = math.sqrt((bullet.x-player.x)**2 + (bullet.y-player.y)**2)

            if dist < 20:

                player.hp -= bullet.damage

                sparks.append(HitSpark(bullet.x,bullet.y))

                if player.hp <= 0:

                    player.alive = False

                    explosions.append(
                        Explosion(int(player.x),int(player.y))
                    )

                bullets.remove(bullet)
                break



    alive_players = [p for p in players if p.alive]

    if len(alive_players) == 1 and not game_over:

        winner = alive_players[0].name
        game_over = True
        death_timer = pygame.time.get_ticks()



    screen.fill((0,0,0))


    for wall in walls:
        pygame.draw.rect(screen,(180,80,40),wall)


    for player in players:
        player.draw(screen,font)


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
