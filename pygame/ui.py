import pygame

def draw_hp(player,x,y,screen,font):

    hp=max(0,player.hp)

    text=font.render(f"HP: {hp}",True,(255,255,255))
    screen.blit(text,(x,y))

    pygame.draw.rect(screen,(100,0,0),(x,y+30,200,20))
    pygame.draw.rect(screen,(0,255,0),(x,y+30,hp*2,20))