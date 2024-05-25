import pygame
import utils

from gamemap import Map
from gameplayer import Player
from keyboard import KeyboardController
from commands import Commands
from sprites import StaticSprite, Animation, Sprites
from Vec2d import Vector2D

def ComputeMapSpritePosition(DisplaySize, MapSpriteSize):
    return (DisplaySize - MapSpriteSize) // 2

def GenMapSprite(gmap, images):
    
    d = gmap.data()
    w = gmap.width()
    h = gmap.height()
    fieldsize = images.GetFieldSize()
    
    imgw = w*fieldsize
    imgh = h*fieldsize
    MapSprite = StaticSprite(pygame.Rect(0, 0, imgw, imgh), pygame.Surface([imgw, imgh]) );    
    MapLine = 0

    for y in range(h):
        for x in range(w):
            sprite = images.GetStaticSprite(d[MapLine + x])
            MapSprite.image.blit(sprite.image, (x*fieldsize, y*fieldsize), sprite.rect)
        MapLine += w
    
    return MapSprite

class Game:    
    
    def __init__(self, cfg, images, keys):
        self.m_Cfg = cfg
        self.m_Images = images
        self.m_Map = Map(cfg["map"])
        self.m_Players = [];
        self.m_Commands = Commands()
        self.m_Keyboard = keys
        for i,p in enumerate(cfg["players"]):
            self.m_Players.append(self._CreatePlayer(i, p))
        self.m_MapSprite = GenMapSprite(self.m_Map, images)
        self.m_MapSprite.position = ComputeMapSpritePosition(
            Vector2D(*self.m_Cfg["display_size"]), 
            Vector2D(*self.m_MapSprite.rect.size))
    
    def _CreatePlayer(self, index, cfg) -> Player:
        t = cfg["type"]
        if t != 'key':
            raise utils.Error("Invalid player type: " + t)
        cfg["position"] = self.m_Map.positions()[index]
        cfg["step"] = self.m_Cfg["step"]
        p = Player(cfg, self)
        c = KeyboardController(cfg["keys"], p, self.m_Keyboard)
        p.m_Controller = c
        return p

    def AddCmd(self, cmd):
        pass
    
    def GetMapSprite(self):
        return self.m_MapSprite
    
    def GetCfg(self):
        return self.m_Cfg

    def GetPlayers(self):
        return self.m_Players

    def GetAnimation(self, anim):
        return self.m_Images.GetAnimation(anim)
    
    def Update(self):  
        self.m_Keyboard.Update()
        for p in self.m_Players:
            p.Update()

    def ToPixelPos(self, pos):        
        origin = self.m_MapSprite.position
        f = self.m_Images.GetFieldSize()
        return origin + pos*f//100   
   
def DrawGame(g, screen):
    MapSprite = g.GetMapSprite()
    screen.DrawSprite(MapSprite, MapSprite.position)
    

    for p in g.GetPlayers():
        pos = g.ToPixelPos(p.GetPosition())
        playersprite = p.GetSprite()
        screen.DrawSprite(playersprite, pos)     

    

