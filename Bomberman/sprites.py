from dataclasses import Field
from os import times
from re import S
import string
import pygame
from Vec2d import Vector2D
from utils import DirToVec

def RectFromField(field, index, fieldsize):
    return pygame.Rect((field[0] + index)*fieldsize, field[1]*fieldsize, fieldsize, fieldsize)           

class StaticSprite(pygame.sprite.Sprite):
    def __init__(self, rect, image):
        pygame.sprite.Sprite.__init__(self)
        self.rect = rect
        self.image = image

class Animation:
    def __init__(self, sprites):
        self.sprites = sprites
        self.m_Phase = 0
        
    def NextPhase(self):
        self.m_Phase = (self.m_Phase + 1) % len(self.sprites)
        
    def SetPhase(self, phase:int):
        self.m_Phase = phase

    def GetCurrent(self):
        s = self.sprites[self.m_Phase]        
        return s

    def size(self):
        return len(self.sprites)

    def GetNext(self):
        self.NextPhase()
        return self.GetCurrent()  

def ParseTimeToTicks(TimeStr:string, fps:int):
    TickInMS = 1000//fps
    if TimeStr.endswith('ms'):
        ms = int(TimeStr[:-2])
        return ms*TickInMS
    if TimeStr.endswith('s'):
        s = int(TimeStr[:-1])
        return s*1000*TickInMS
    if TimeStr.endswith('t'):
        return int(TimeStr[:-1])
    
class TimeLine:
    def __init__(self, cfg):
        self.m_Time = ParseTimeToTicks(cfg["time"])
        self.m_Data = cfg["data"]
        self.m_Counter = 0

    def GetPhaseForTick(num):
        pass


    
class FireCross:
    def __init__(self, cfg, image, fieldsize):
        self.m_Image = image
        self.m_Cfg = cfg;
        self.m_FieldSize = fieldsize
        
        self.m_CenterAnimation = self._AnimFromOffset(Vector2D(0,0))
        self.m_MidAnimation = {}
        self.m_EndAnimation = {}

        
        for d, v in DirToVec.items():
            self.m_MidAnimation[d] = self._AnimFromOffset(v);
            self.m_EndAnimation[d] = self._AnimFromOffset(2*v)
        
    
    def GetCentralAnimation(self) -> Animation:
        return self.m_CenterAnimation
    
    def GetMidAnimation(self, dir) -> Animation:
        return self.m_MidAnimation[dir]
    
    def GetEndAnimation(self, dir) -> Animation:
        return self.m_EndAnimation[dir]
   
    def _AnimFromOffset(self, FieldInCross:Vector2D):
        crosses = self.m_Cfg
        sprites = []
        for c in crosses:
            FieldInImage = Vector2D(*c) + FieldInCross
            rect = RectFromField(FieldInImage.to_tuple(), 0, self.m_FieldSize)
            sprites.append(StaticSprite(rect, self.m_Image))
        return sprites
    
    def Draw(self, scr, fire, size, phase):
        counts = fire["counts"]
        pos = fire["pos"]
        scr.DrawSprite(self.m_CenterAnimation[phase], pos)
        for i, dv in enumerate(DirToVec.values()):            
            for j in range(counts[i]):
                fp = pos + dv*j
                scr.DrawSprite(self.m_EndAnimation[phase] if j == size else self.m_MidAnimation[phase], fp)
    

class Sprites:
    def __init__(self, cfg):
        self.m_Cfg = cfg                
        self.m_Image = pygame.image.load(self.m_Cfg["name"]).convert_alpha()
        self.m_Image.set_colorkey(self.m_Cfg["transparent_color"]) 
        self.m_FieldSize = self.m_Cfg["fieldsize"]
        self.m_Fields = {}
        for k, v in self.m_Cfg["fields"].items():
            self.m_Fields[k] = self._GenSprites(v)
        self.m_FireCross = FireCross(self.m_Cfg["cross"], self.m_Image, self.m_FieldSize)
        
    def GetStaticSprite(self, field):
        return self.m_Fields[field][0]
    
    def _GenSprites(self, field):
        sprites = []
        for i in range(field[2]):
            sprites.append(StaticSprite(RectFromField(field, i, self.m_FieldSize), self.m_Image))
        return sprites

    def GetAnimation(self,fieldname):
        return Animation(self.m_Fields[fieldname])
    
    def GetFieldSize(self):
        return self.m_FieldSize
    
    def GetFireCross(self):
        return self.m_FireCross
    
        

