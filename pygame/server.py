import zmq
import random
import pygame
from player import Player
from weapon import Weapon
from map import generate_walls
from setting import WIDTH, HEIGHT
from bullet import Bullet

pygame.init()

# ZMQ setup
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:2345")
print("Server gestart")

# Game state
players = {}
bullets = []
weapon = Weapon("Pistol",12,400)
walls = generate_walls()

# Spawnpunten (4 hoeken)
spawn_points = [
    (80, 80),
    (WIDTH-80, 80),
    (80, HEIGHT-80),
    (WIDTH-80, HEIGHT-80)
]

while True:
    data = socket.recv_pyobj()
    name = data["name"]
    dx = data["dx"]
    dy = data["dy"]
    shoot = data["shoot"]

    # Speler aanmaken als nieuw
    if name not in players:
        spawn = spawn_points[len(players) % len(spawn_points)]
        color = (
            random.randint(100,255),
            random.randint(100,255),
            random.randint(100,255)
        )
        players[name] = Player(spawn[0], spawn[1], color, weapon, name)

    player = players[name]

    # Beweging
    player.move(dx, dy, WIDTH, HEIGHT)
    if dx != 0 or dy != 0:
        player.dir_x = dx
        player.dir_y = dy

    # Schieten
    if shoot:
        player.shoot(bullets, [], player.x, player.y)

    # Update bullets
    for bullet in bullets[:]:
        bullet.update()
        # Botsing met muur
        for wall in walls:
            if wall.collidepoint(bullet.x, bullet.y):
                bullets.remove(bullet)
                break
        # Botsing met spelers
        for p in players.values():
            if p == bullet.owner or not p.alive:
                continue
            dist = ((bullet.x - p.x)**2 + (bullet.y - p.y)**2)**0.5
            if dist < 15:
                p.hp -= bullet.damage
                if p.hp <= 0:
                    p.alive = False
                bullets.remove(bullet)
                break
        # Buiten scherm
        if bullet.x < 0 or bullet.x > WIDTH or bullet.y < 0 or bullet.y > HEIGHT:
            if bullet in bullets:
                bullets.remove(bullet)
    
    # State maken
    state = {"players": [], "bullets": []}
    for p in players.values():
        state["players"].append({
            "name": p.name,
            "x": p.x,
            "y": p.y,
            "hp": p.hp,
            "color": p.color,
            "alive": p.alive
        })
    for b in bullets:
        state["bullets"].append({
            "x": b.x,
            "y": b.y
        })

    socket.send_pyobj(state)