from asyncio.windows_events import NULL
import pygame

IMAGE = NULL

def Init():
    global IMAGE
    IMAGE = pygame.image.load('player.png').convert_alpha()
    

class Player(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        self.image = IMAGE
        self.rect = self.image.get_rect(center=pos)