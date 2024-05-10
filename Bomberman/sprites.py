import pygame

class StaticSprite(pygame.sprite.Sprite):
    def __init__(self, rect, image):
        pygame.sprite.Sprite.__init__(self)
        self.rect = rect
        self.image = image

class Animation:
    def __init__(self, sprites):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = sprites
        self.m_Phase = 0
        
    def NextPhase(self):
        self.m_Phase = (self.m_Phase + 1) % len(self.sprites)

    def GetCurrent(self):
        s = self.sprites[self.m_Phase]        
        return s

    def GetNext(self):
        self.NextPhase()
        return self.GetCurrent( )        
    

class Sprites:
    def __init__(self, cfg):
        self.m_Cfg = cfg                
        self.m_Image = pygame.image.load(self.m_Cfg["name"]).convert_alpha()
        self.m_Image.set_colorkey(self.m_Cfg["transparent_color"]) 
        self.m_FieldSize = self.m_Cfg["fieldsize"]
        self.m_Fields = {}
        for k, v in self.m_Cfg["fields"].items():
            self.m_Fields[k] = self._GenSprites(v)
        
    def GetStaticSprite(self, field):
        return self.m_Fields[field].sprites[0]
    
    def _RectFromField(self, field, index):
        return pygame.Rect((field[0] + index)*self.m_FieldSize, field[1]*self.m_FieldSize, self.m_FieldSize, self.m_FieldSize)
            
    def _GenSprites(self, field):
        sprites = []
        for i in range(field[2]):
            sprites.append(StaticSprite(self._RectFromField(field, i), self.m_Image))
        return Animation(sprites)

    def GetAnimation(self,fieldname):
        return self.m_Fields[fieldname]
    
    def GetFieldSize(self):
        return self.m_FieldSize
        

