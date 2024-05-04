import pygame

class StaticSprite(pygame.sprite.Sprite):
    def __init__(self, rect, img):
        pygame.sprite.Sprite.__init__(self)
        self.rect = rect
        self.img = img

class Animation:
    def __init__(self, sprites):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = sprites
        self.m_Phase = 0
        
    def GetNext(self):
        s = self.sprites[self.phase]
        self.m_Phase = (self.phase + 1) % self.sprites.len()
        return s
    

class Sprites:
    
    class Cfg:
        PicSize = 16, 
        fields = {
            'W': (3,3, 1), 
            'w': (3,3, 6),
            'b': (3,3, 3),   
            'L': (0,0, 3),
            'D': (0,3, 3),
            'R': (1,0, 3),
            'U': (1,3, 3),
        }

    def __init__(self, cfg, img):
        self.m_Cfg = cfg
        self.m_Image = img
        self.m_PicSize = self.m_Cfg["PicSize"]
        self.m_Fields = {}
        for k in self.m_Cfg.fields:
            v = self.m_Cfg.fields[k]
            self.m_Fields[k] = self._GenSprites(v)
        
    def GetStaticSprite(self, field):
        return self.m_Fields[field][0]
    
    def _RectFromField(self, field, index):
        return pygame.Rect((field[0] + index)*self.m_PicSize, field[1]*self.m_PicSize, self.m_PicSize, self.m_PicSize)
            
    def _GenSprites(self, field):
        sprites = []
        for i in range(field[2]):
            sprites.append(StaticSprite(self._RectFromField(field, i), self.m_Image))

    def GetAnimation(self,fieldname):
        return self.m_Fields(fieldname)
        

