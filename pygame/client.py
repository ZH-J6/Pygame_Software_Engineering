import sys
import zmq
import pygame

from player import Player
from weapon import Weapon
from ui import draw_hp
from setting import WIDTH, HEIGHT

pygame.init()

name = sys.argv[1]

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:2345")

screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

font = pygame.font.SysFont(None,36)

players = {}
weapon = Weapon("Pistol",12,400)

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    dx = 0
    dy = 0
    shoot = False

    if keys[pygame.K_w] or keys[pygame.K_UP]: dy = -1
    if keys[pygame.K_s] or keys[pygame.K_DOWN]: dy = 1
    if keys[pygame.K_a] or keys[pygame.K_LEFT]: dx = -1
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]: dx = 1

    if keys[pygame.K_SPACE]:
        shoot = True

    action = {
        "name": name,
        "dx": dx,
        "dy": dy,
        "shoot": shoot
    }

    socket.send_pyobj(action)
    state = socket.recv_pyobj()

    screen.fill((20,20,40))

    # spelers updaten
    for pdata in state["players"]:

        pname = pdata["name"]

        if pname not in players:
            players[pname] = Player(
                pdata["x"],
                pdata["y"],
                pdata["color"],
                weapon,
                pname
            )

        p = players[pname]

        p.x = pdata["x"]
        p.y = pdata["y"]
        p.hp = pdata["hp"]

        p.draw(screen,font)

    # HP tekenen
    i = 0
    for p in players.values():
        draw_hp(p,20,20 + i*60,screen,font)
        i += 1

    # bullets tekenen
    for b in state["bullets"]:

        pygame.draw.circle(
            screen,
            (255,220,50),
            (int(b["x"]),int(b["y"])),
            5
        )

    pygame.display.flip()

    clock.tick(60)

pygame.quit()