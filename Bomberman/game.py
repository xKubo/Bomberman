import diag
import pygame
import utils

from gamemap import Map
from gameplayer import Player
from keyboard import KeyboardController
from commands import Commands
from sprites import StaticSprite, Animation, Sprites
from Vec2d import Vector2D

from arena import Arena

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
            t = d[MapLine + x]
            if t == 'w':    # remove destroyable walls from permanent map image
                t = ' '
            sprite = images.GetStaticSprite(t)
            MapSprite.image.blit(sprite.image, (x*fieldsize, y*fieldsize), sprite.rect)
        MapLine += w
    
    return MapSprite

class Game:    
    
    def __init__(self, cfg, images:Sprites, createcontroller, screen):
        self.m_Screen = screen
        self.m_Screen.ToPixelPos = self.ToPixelPos
        self.m_Cfg = cfg
        self.m_Images = images 
        self.m_Map = Map(cfg["map"])
        self.m_FieldTolerance = int(100*self.m_Cfg["field_tolerance"]) 
        self.m_Arena = Arena(self.m_Map, self.m_FieldTolerance, self.m_Images)
        self.m_Players = [];
        self.m_Commands = Commands()
        self.m_CreateController = createcontroller
        defaults = self.m_Cfg["player_defaults"]
        utils.UpdateTimeToTicks(defaults, ["bomb_time"], images.TickMS())
        for i,p in enumerate(cfg["players"]):
            cfg = {**p, **defaults} # merge player_defaults with player cfg
            self.m_Players.append(self._CreatePlayer(i, cfg))
        self.m_MapSprite = GenMapSprite(self.m_Map, images)
        self.m_MapSprite.position = ComputeMapSpritePosition(
            Vector2D(*self.m_Cfg["display_size"]), 
            Vector2D(*self.m_MapSprite.rect.size))       
    
    def _CreatePlayer(self, index, cfg) -> Player:
        cfg["position"] = self.m_Map.positions()[index]        
        p = Player(cfg, self)
        c = self.m_CreateController(cfg, p)
        p.m_Controller = c
        return p

    def GetFieldSize(self):
        return self.m_Images.GetFieldSize();

    def AddCmd(self, cmd):
        pass
    
    def GetMapSprite(self):
        return self.m_MapSprite
    
    def GetCfg(self):
        return self.m_Cfg

    def GetPlayers(self):
        return self.m_Players

    def GetAnimation(self, anim):
        return self.m_Images.CreateFieldAnimation(anim)
    
    def Update(self):  
        self.m_Arena.Update()
        for p in self.m_Players:
            p.Update()   
         
    
    def Arena(self):
        return self.m_Arena

    def ToPixelPos(self, pos):        
        origin = self.m_MapSprite.position
        f = self.m_Images.GetFieldSize()
        return origin + pos*f//100   
   
    def Draw(self):
        
        scr = self.m_Screen
        t = self.m_Images.Text()

        
        MapSprite = self.GetMapSprite()
        self.m_Screen.DrawSprite(MapSprite, Vector2D(0,0))
    
        t.SetPos(Vector2D(0,0))
        ShowArena(scr, t, self.m_Arena)    
        self.m_Arena.Draw(scr)


        t.SetPos(Vector2D(self.m_Map.width()*24, 0))
        for p in self.GetPlayers():
            pos = p.Position()           
            neighbors = list(utils.NeighboringFields(pos,self.m_FieldTolerance))            
            neighbors.sort(key=lambda v : v.to_tuple())
            t.PrintLn(scr, f"{p.Name()}:{pos}:BF{utils.BestField(pos)}:NF{neighbors}:{p.GetStatus()}");
            p.Draw(scr)

def ShowArena(scr, text, arena:Arena):
    (w, h) = arena.GetExtents()
    fields = arena.GetFields()
    for y in range(h):
        s = ""
        for x in range(w):
            f = fields[y*w + x]
            s += f.Type()
        text.PrintLn(scr, s)
    