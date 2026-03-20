import sys
import zmq
import pygame

from player import Player
from weapon import Weapon
from setting import WIDTH, HEIGHT
from map import generate_walls
from effects import Explosion, HitSpark

pygame.init()

name = sys.argv[1] if len(sys.argv) > 1 else "Player"

# ZMQ setup
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:2345")

pygame.mixer.music.load("assets/bgm2.mp3")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

players = {}
weapon = Weapon("Missile", 12, 400)
walls = generate_walls()

explosions = []
sparks = []

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Input
    keys = pygame.key.get_pressed()
    dx = dy = 0
    shoot = False

    if keys[pygame.K_w]: dy = -1
    if keys[pygame.K_s]: dy = 1
    if keys[pygame.K_a]: dx = -1
    if keys[pygame.K_d]: dx = 1

    if keys[pygame.K_UP]: dy = -1
    if keys[pygame.K_DOWN]: dy = 1
    if keys[pygame.K_LEFT]: dx = -1
    if keys[pygame.K_RIGHT]: dx = 1

    if keys[pygame.K_SPACE] or keys[pygame.K_f]:
        shoot = True

    # Send action
    action = {"name": name, "dx": dx, "dy": dy, "shoot": shoot}
    socket.send_pyobj(action)
    state = socket.recv_pyobj()

    # Check if player was killed
    if name in state["dead_players"]:
        print("You were destroyed!")
        pygame.quit()
        sys.exit()

    # Effects
    for ex in state["explosions"]:
        explosions.append(Explosion(int(ex[0]), int(ex[1])))
    for sp in state["sparks"]:
        sparks.append(HitSpark(int(sp[0]), int(sp[1])))

    # Render
    screen.fill((0, 0, 0))

    # Draw walls
    for wall in walls:
        pygame.draw.rect(screen, (180, 80, 40), wall)

    # Draw players
    for pdata in state["players"]:
        pname = pdata["name"]

        if pname not in players:
            players[pname] = Player(
                pdata["x"], pdata["y"], pdata["color"], weapon, pname
            )

        p = players[pname]
        p.x = pdata["x"]
        p.y = pdata["y"]
        p.hp = pdata["hp"]
        p.dir_x = pdata["dir_x"]
        p.dir_y = pdata["dir_y"]

        p.draw(screen, font)

    # Draw bullets
    for b in state["bullets"]:
        pygame.draw.circle(screen, (255, 220, 50), (int(b["x"]), int(b["y"])), 5)
        pygame.draw.circle(screen, (255, 120, 0), (int(b["x"]), int(b["y"])), 3)

    # Draw effects
    for e in explosions[:]:
        e.update()
        e.draw(screen)
        if len(e.particles) == 0:
            explosions.remove(e)

    for s in sparks[:]:
        s.update()
        s.draw(screen)
        if len(s.particles) == 0:
            sparks.remove(s)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()