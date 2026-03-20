"""
Multiplayer server module for Tank Battle.

Handles:
- Player connections and disconnections via ZMQ.
- Player movement, shooting, and collisions with walls.
- Bullet updates and player damage/death.
- One-frame events like explosions and sparks.
- Sending the current game state to all connected clients.

Protocol:
- Uses ZMQ REP socket on tcp://*:2345.
- Receives player actions as Python objects:
    {"name": str, "dx": int, "dy": int, "shoot": bool}
- Sends back game state including:
    {
        "players": [...],
        "bullets": [...],
        "explosions": [...],
        "sparks": [...],
        "dead_players": [...]
    }
"""

import zmq
import random
import pygame
import math
import time

from player import Player
from weapon import Weapon
from map import generate_walls
from setting import WIDTH, HEIGHT

pygame.init()

# ZMQ setup
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:2345")

print("Server started")

# Game state
players = {}  # name -> {"obj": Player, "last_seen": time}
bullets = []
weapon = Weapon("Missile", 12, 400)
walls = generate_walls()

explosions = []
sparks = []
dead_players = []  # players killed this frame
dead_cooldown = {}  # name -> time of death (prevents instant respawn)

# Spawn points for players
spawn_points = [
    (80, 80),
    (WIDTH - 80, 80),
    (80, HEIGHT - 80),
    (WIDTH - 80, HEIGHT - 80)
]

def move_with_collision(player, dx, dy):
    """Move player and handle wall collision"""
    old_x, old_y = player.x, player.y
    player.move(dx, dy, WIDTH, HEIGHT)

    rect = pygame.Rect(player.x - 20, player.y - 20, 40, 40)

    for wall in walls:
        if rect.colliderect(wall):
            player.x = old_x
            player.y = old_y
            break

while True:
    data = socket.recv_pyobj()
    name = data["name"]
    dx = data["dx"]
    dy = data["dy"]
    shoot = data["shoot"]

    now = time.time()

    # If player recently died, force them to exit (no instant respawn)
    if name in dead_cooldown:
        if now - dead_cooldown[name] < 2:  # 2-second block
            state = {
                "players": [],
                "bullets": [],
                "explosions": [],
                "sparks": [],
                "dead_players": [name]
            }
            socket.send_pyobj(state)
            continue
        else:
            del dead_cooldown[name]

    # Create new player if not exists
    if name not in players:
        spawn = random.choice(spawn_points)
        color = (
            random.randint(100, 255),
            random.randint(100, 255),
            random.randint(100, 255)
        )
        players[name] = {
            "obj": Player(spawn[0], spawn[1], color, weapon, name),
            "last_seen": now
        }
        print(f"{name} joined the game")

    player_data = players[name]
    player = player_data["obj"]
    player_data["last_seen"] = now  # update heartbeat

    # Move player
    move_with_collision(player, dx, dy)
    if dx != 0 or dy != 0:
        player.dir_x = dx
        player.dir_y = dy

    # Shooting
    if shoot:
        spawn_x = player.x + player.dir_x * 25
        spawn_y = player.y + player.dir_y * 25
        player.shoot(bullets, [], spawn_x, spawn_y)

    # Update bullets
    for bullet in bullets[:]:
        bullet.update()

        # Out of bounds
        if bullet.x < 0 or bullet.x > WIDTH or bullet.y < 0 or bullet.y > HEIGHT:
            bullets.remove(bullet)
            continue

        # Wall collision
        hit_wall = False
        for wall in walls:
            if wall.collidepoint(bullet.x, bullet.y):
                sparks.append((bullet.x, bullet.y))
                bullets.remove(bullet)
                hit_wall = True
                break
        if hit_wall:
            continue

        # Hit player
        for pname in list(players.keys()):
            p = players[pname]["obj"]

            if p == bullet.owner:
                continue

            dist = math.sqrt((bullet.x - p.x) ** 2 + (bullet.y - p.y) ** 2)
            if dist < 20:
                p.hp -= bullet.damage
                sparks.append((bullet.x, bullet.y))

                if p.hp <= 0:
                    explosions.append((p.x, p.y))
                    dead_players.append(pname)
                    dead_cooldown[pname] = time.time()
                    del players[pname]
                    print(f"{pname} was destroyed by {bullet.owner.name}")

                bullets.remove(bullet)
                break

    # Remove disconnected players
    timeout = 0.3
    for pname in list(players.keys()):
        if now - players[pname]["last_seen"] > timeout:
            print(f"{pname} disconnected")
            del players[pname]

    # Build state
    state = {
        "players": [],
        "bullets": [],
        "explosions": explosions,
        "sparks": sparks,
        "dead_players": dead_players
    }

    for pdata in players.values():
        p = pdata["obj"]
        state["players"].append({
            "name": p.name,
            "x": p.x,
            "y": p.y,
            "hp": p.hp,
            "color": p.color,
            "dir_x": p.dir_x,
            "dir_y": p.dir_y
        })

    for b in bullets:
        state["bullets"].append({"x": b.x, "y": b.y})

    # Clear one-frame events
    explosions = []
    sparks = []
    dead_players = []

    socket.send_pyobj(state)