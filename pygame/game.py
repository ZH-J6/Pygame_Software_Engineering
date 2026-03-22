"""
Local game loop for Tank Battle.

Handles:
- Initializing Pygame and setting up the screen.
- Start menu screen with controls overview.
- Loading assets (background music, fonts, images).
- Player movement, shooting, and collision handling.
- Bullet updates, collisions with walls and players.
- Visual effects (explosions, muzzle flashes, hit sparks).
- Rendering players, bullets, walls, and effects.
- Detecting game over conditions and displaying winner.
"""

import pygame
import math

from setting import WIDTH, HEIGHT, FPS
from player import Player
from weapon import Weapon
from bullet import Bullet
from effects import Explosion, MuzzleFlash, HitSpark
from map import generate_walls

pygame.init()
pygame.mixer.music.load("assets/bgm2.mp3")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)
shoot_sound = pygame.mixer.Sound("assets/shoot.wav")
shoot_sound.set_volume(0.2)
explosion_sound = pygame.mixer.Sound("assets/explosion.wav")
explosion_sound.set_volume(0.4)

font = pygame.font.SysFont(None,20)
big_font = pygame.font.SysFont(None,80)

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Tank Battle")

clock = pygame.time.Clock()

def draw_start_menu():
    screen.fill((10, 10, 20))
    title = big_font.render("TANK BATTLE", True, (255, 200, 0))
    screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100)))
    sub = font.render("Press ENTER to start", True, (255, 255, 255))
    screen.blit(sub, sub.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
    p1 = font.render("P1: WASD + F to shoot", True, (100, 255, 100))
    p2 = font.render("P2: Arrow Keys + L to shoot", True, (255, 100, 100))
    screen.blit(p1, p1.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60)))
    screen.blit(p2, p2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 90)))
    pygame.display.flip()

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

# Start menu
in_menu = True
while in_menu:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                in_menu = False
    draw_start_menu()

running = True
winner = None
game_over = False
death_timer = 0


def move_with_collision(player,dx,dy):
    """
    Move the player and handle collision with walls.

    Args:
        player: Player object to move.
        dx, dy: Movement direction.
    """
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
        shoot_sound.play()


    if not game_over and keys[pygame.K_l]:

        spawn_x = players[1].x + players[1].dir_x * 25
        spawn_y = players[1].y + players[1].dir_y * 25

        players[1].shoot(bullets,flashes,spawn_x,spawn_y)
        shoot_sound.play()



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
                    explosion_sound.play()

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
