import pygame

class StaticSprite(pygame.sprite.Sprite):
    def __init__(self, rect, img):
        pygame.sprite.Sprite.__init__(self)
        self.rect = rect
        self.img = img

class Animation(pygame.sprite.Sprite):
    def __init__(self, sprites):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = sprites
    

class Images:
    
    class Cfg:
        PicSize = 16, 
        fields = {
            'W': (3,3, 1), 
            'w': (3,3, 6),
            'b': (3,3, 3),      
        }

    def __init__(self, cfg, img):
        self.cfg = cfg
        self.image = img
        
    def GetStaticSprite(field):
        pass

    def GetAnimation(field):
        pass
        

