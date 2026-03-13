import pygame
from setting import WIDTH, HEIGHT

TILE = 40

# B = 砖墙
# S = 钢墙
# . = 空地
# X = 边界

MAP = [

"XXXXXXXXXXXXXXXXXXXX",
"X....B....B....B...X",
"X....B....B....B...X",
"X....B....B....B...X",
"X..................X",
"X..BBB......BBB....X",
"X..................X",
"X....S......S......X",
"X..................X",
"X....BBB....BBB....X",
"X..................X",
"X....B....B....B...X",
"X....B....B....B...X",
"X....B....B....B...X",
"XXXXXXXXXXXXXXXXXXXX"

]

def generate_walls():

    walls = []

    for row, line in enumerate(MAP):
        for col, cell in enumerate(line):

            x = col * TILE
            y = row * TILE

            if cell in ["B","S","X"]:

                walls.append(
                    pygame.Rect(x,y,TILE,TILE)
                )

    return walls