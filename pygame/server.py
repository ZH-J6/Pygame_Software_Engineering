import zmq
import random
import pygame

from player import Player
from weapon import Weapon
from setting import WIDTH, HEIGHT

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:2345")

print("Server gestart")

players = {}
bullets = []

weapon = Weapon("Pistol",12,400)

while True:

    data = socket.recv_pyobj()

    name = data["name"]
    dx = data["dx"]
    dy = data["dy"]
    shoot = data["shoot"]

    # speler maken
    if name not in players:

        x = random.randint(100,700)
        y = random.randint(100,500)

        color = (
            random.randint(100,255),
            random.randint(100,255),
            random.randint(100,255)
        )

        players[name] = Player(x,y,color,weapon,name)

    player = players[name]

    player.move(dx,dy,WIDTH,HEIGHT)

    if shoot:
        player.shoot(bullets,[])

    for bullet in bullets:
        bullet.update()

    # state maken
    state = {
        "players": [],
        "bullets": []
    }

    for p in players.values():
        state["players"].append({
            "name": p.name,
            "x": p.x,
            "y": p.y,
            "hp": p.hp,
            "color": p.color
        })

    for b in bullets:
        state["bullets"].append({
            "x": b.x,
            "y": b.y
        })

    socket.send_pyobj(state)