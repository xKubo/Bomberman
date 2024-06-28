from screen import Screen
import utils
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
    def __init__(self, sprites, timelinedata):
        self.m_Timeline = TimeLine(timelinedata, len(sprites))
        self.sprites = sprites
        
    def size(self):
        return len(self.sprites)
    
    def Update(self):
        self.m_Timeline.Update();
    
    def Draw(self, scr:Screen, pos:Vector2D):
        sprite = self.sprites[self.m_Timeline.CurrentFrame()]        
        scr.DrawSprite(sprite, pos)
        
    def TotalTicks(self):
        return self.m_Timeline.TotalTicks()



    
class TimeLine:
    def __init__(self, cfg, spritecount):
        self.m_FrameTime = cfg["frame_time"]
        self.m_Frames = cfg["frames"]
        self.m_TickMS = cfg["tick_ms"]
        self.m_CurrentFrame = 0
        if not self.m_Frames:
            self.m_Frames = [i for i in range(spritecount)]
        self.m_TotalTime = self.m_FrameTime*len(self.m_Frames)
        self.m_TotalTicks = self.m_TotalTime / self.m_TickMS
        self.m_Time = 0

    def TotalTime(self):
        return self.m_TotalTime

    def TotalTicks(self):
        return self.m_TotalTicks

    def CurrentFrame(self):
        return self.m_Frames[self.m_CurrentFrame]

    def Update(self):
        self.m_Time += self.m_TickMS
        while self.m_Time > self.m_FrameTime:
            self.m_CurrentFrame += 1
            self.m_CurrentFrame %= len(self.m_Frames)
            self.m_Time -= self.m_FrameTime
        
    
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

    def size(self):
        return len(self.m_Cfg)
    
    def Draw(self, scr, fire, phase):
        pos = fire["pos"]
        size = fire["size"]
        counts = fire["counts"]
        scr.DrawSprite(self.m_CenterAnimation[phase], pos)
        for i, (d,v) in enumerate(DirToVec.items()):
            for j in range(1, counts[i] + 1):
                fp = pos + v*j*100
                a = self.m_EndAnimation[d][phase] if j == size else self.m_MidAnimation[d][phase]
                scr.DrawSprite(a, fp)
                
class FireCrossAnimation:
    def __init__(self, cross:FireCross, timelinecfg):
        self.m_Timeline = TimeLine(timelinecfg, cross.size())
        self.m_Cross = cross
        
    def Update(self):
        self.m_Timeline.Update()
        
    def TotalTime(self):
        return self.m_Timeline.TotalTime()

    def TotalTicks(self):
         return self.m_Timeline.TotalTicks()
    
    def Draw(self, scr, fire):
        self.m_Cross.Draw(scr, fire, self.m_Timeline.CurrentFrame())

class Sprites:
    def __init__(self, cfg, fps:int):
        self.m_TickMS = 1000//fps
        self.m_Cfg = cfg                
        self.m_Image = pygame.image.load(self.m_Cfg["name"]).convert_alpha()
        self.m_FieldSize = self.m_Cfg["fieldsize"]
        sf = self.m_Cfg["scale_factor"]
        if sf != 1:
            self.m_Image = pygame.transform.scale_by(self.m_Image, sf)
            self.m_FieldSize *= sf
            
        self.m_Image.set_colorkey(self.m_Cfg["transparent_color"]) 
        
        self.m_Fields = {}
        for k, v in self.m_Cfg["fields"].items():
            self.m_Fields[k] = self._GenSprites(v)
        self.m_TimelineData = {}
        for keys, v in self.m_Cfg["animations"].items():
            for c in keys:
                cfg = utils.ParseTimeLineCfg(v)
                cfg["tick_ms"] = self.m_TickMS
                self.m_TimelineData[c] = cfg
        self.m_FireCross = FireCross(self.m_Cfg["cross"], self.m_Image, self.m_FieldSize)
        
    def TickMS(self):
        return self.m_TickMS
        
    def GetStaticSprite(self, field):
        return self.m_Fields[field][0]
    
    def _GenSprites(self, field):
        sprites = []
        for i in range(field[2]):
            sprites.append(StaticSprite(RectFromField(field, i, self.m_FieldSize), self.m_Image))
        return sprites

    def CreateFieldAnimation(self,fieldname):
        return Animation(self.m_Fields[fieldname], self.m_TimelineData[fieldname])
    
    def GetFieldSize(self):
        return self.m_FieldSize
    
    def CreateCrossAnimation(self):
        return FireCrossAnimation(self.m_FireCross, self.m_TimelineData['f']);
            

