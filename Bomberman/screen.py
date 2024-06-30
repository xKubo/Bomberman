import pygame
from Vec2d import Vector2D

class Screen:
    def __init__(self, scr:pygame.Surface):
        self.m_Screen = scr      
        
    def DrawSprite(self, sprite, pos):
        pixelpos = self.ToPixelPos(pos)     # set up by game class to convert the game position to pixel position
        self.DrawSpritePix(sprite, pixelpos)
        
    def DrawSpritePix(self, sprite, pixelpos):
        self.m_Screen.blit(sprite.image, pixelpos.to_tuple(), sprite.rect)  