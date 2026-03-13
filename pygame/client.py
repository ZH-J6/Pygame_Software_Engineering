import sys
import zmq
import pygame

WIDTH = 800
HEIGHT = 600

name = sys.argv[1]

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:2345")

pygame.init()

screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

running = True
game_state = None

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    dx = 0
    dy = 0
    shoot = False

    if keys[pygame.K_w]: dy = -1
    if keys[pygame.K_s]: dy = 1
    if keys[pygame.K_a]: dx = -1
    if keys[pygame.K_d]: dx = 1

    if keys[pygame.K_SPACE]:
        shoot = True

    action = {
        "name": name,
        "dx": dx,
        "dy": dy,
        "shoot": shoot
    }

    socket.send_pyobj(action)

    game_state = socket.recv_pyobj()

    screen.fill((20,20,40))

    # spelers tekenen
    for player in game_state["players"].values():

        pygame.draw.circle(
            screen,
            player.color,
            (int(player.x),int(player.y)),
            15
        )

    # bullets tekenen
    for bullet in game_state["bullets"]:

        pygame.draw.circle(
            screen,
            (255,220,50),
            (int(bullet.x),int(bullet.y)),
            5
        )

    pygame.display.flip()

    clock.tick(60)

pygame.quit()