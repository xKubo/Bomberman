from dataclasses import field
import gamemap
import gameplayer
import sprites
import keyboard
import utils
import commands
import pygame

def ComputeMapSpritePosition(DisplaySize, MapSpriteSize):
    (dx, dy) = DisplaySize
    (sx, sy) = MapSpriteSize
    return ((dx - sx) // 2, (dy - sy) // 2)

def GenMapSprite(gmap, images):
    
    d = gmap.data()
    w = gmap.width()
    h = gmap.height()
    fieldsize = images.GetFieldSize()
    
    imgw = w*fieldsize
    imgh = h*fieldsize
    MapSprite = sprites.StaticSprite(pygame.Rect(0, 0, imgw, imgh), pygame.Surface([imgw, imgh]) );    
    MapLine = 0

    for y in range(h):
        for x in range(w):
            sprite = images.GetStaticSprite(d[MapLine + x])
            MapSprite.image.blit(sprite.image, (x*fieldsize, y*fieldsize), sprite.rect)
        MapLine += w
    
    return MapSprite

class Game:    
    
    def __init__(self, cfg, images, keys) -> None:
        self.m_Cfg = cfg
        self.m_Images = images
        self.m_Map = gamemap.Map(cfg["map"])
        self.m_Players = [];
        self.m_Commands = commands.Commands()
        self.m_Keyboard = keys
        for i,p in enumerate(cfg["players"]):
            self.m_Players.append(self._CreatePlayer(i, p))
        self.m_MapSprite = GenMapSprite(self.m_Map, images)
        self.m_MapSprite.position = ComputeMapSpritePosition(self.m_Cfg["display_size"], self.m_MapSprite.rect.size)
    
    def _CreatePlayer(self, index, cfg) -> gameplayer.Player:
        t = cfg["type"]
        if t != 'key':
            raise utils.Error("Invalid player type: " + t)
        cfg["position"] = self.m_Map.positions()[index]
        p = gameplayer.Player(cfg, self)
        c = keyboard.KeyboardController(cfg["keys"], p, self.m_Keyboard)
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
        for p in self.m_Players:
            p.Update()

    def ToPixelPos(self, pos):        
        origin = self.m_MapSprite.position
        fieldsize = self.m_Images.GetFieldSize()
        x = origin[0] + pos[0]*fieldsize//100
        y = origin[1] + pos[1]*fieldsize//100
        return (x, y)    
   
bomb = None

def DrawGame(g, screen):
    MapSprite = g.GetMapSprite()
    screen.blit(MapSprite.image, MapSprite.position)
    

    #for p in g.GetPlayers():
    
    p = g.GetPlayers()[0]
    fs = g.m_Images.GetFieldSize()
    pos = g.ToPixelPos(p.GetPosition())
    pos2 = (pos[0] + fs, pos[1] + fs)
    pos3 = (pos2[0] + fs, pos2[1] + fs)
    
    playersprite = p.GetSprite()
    screen.blit(playersprite.image, pos2, playersprite.rect)     
    

    global bomb
    if bomb == None:
        bomb = g.m_Images.GetAnimation('b')
        
    bs = bomb.GetNext()
    screen.blit(bs.image, pos3, bs.rect)


