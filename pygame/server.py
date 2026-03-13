import zmq
import time
import pygame
import random

from player import Player
from weapon import Weapon
from bullet import Bullet

WIDTH = 800
HEIGHT = 600

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:2345")

print("Server started")

players = {}
bullets = []

weapon = Weapon("Pistol",12,400)

while True:

    data = socket.recv_pyobj()

    name = data["name"]
    dx = data["dx"]
    dy = data["dy"]
    shoot = data["shoot"]

    # speler maken als die nog niet bestaat
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

    # update bullets
    for bullet in bullets:
        bullet.update()

    # game state terugsturen
    state = {
        "players": players,
        "bullets": bullets
    }

    socket.send_pyobj(state)