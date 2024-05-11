import pygame
import utils

from gamemap import Map
from gameplayer import Player
from keyboard import KeyboardController
from commands import Commands
from sprites import StaticSprite, Animation, Sprites
from Vec2d import Vector2D, AsVec2D

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
            AsVec2D(self.m_Cfg["display_size"]), 
            AsVec2D(self.m_MapSprite.rect.size))
    
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
        fieldsize = self.m_Images.GetFieldSize()
        return origin + pos*fieldsize//100   
   
bomb = None

def DrawGame(g, screen):
    MapSprite = g.GetMapSprite()
    screen.blit(MapSprite.image,  MapSprite.position.to_tuple())
    

    #for p in g.GetPlayers():
    
    p = g.GetPlayers()[0]
    fs = g.m_Images.GetFieldSize()
    fsvec = AsVec2D((fs, fs))
    pos = g.ToPixelPos(p.GetPosition())
    pos2 = pos + fsvec
    pos3 = pos2 + fsvec
    
    playersprite = p.GetSprite()
    screen.blit(playersprite.image, pos2.to_tuple(), playersprite.rect)     
    

    global bomb
    if bomb == None:
        bomb = g.m_Images.GetAnimation('b')
        
    bs = bomb.GetNext()
    screen.blit(bs.image, pos3.to_tuple(), bs.rect)


