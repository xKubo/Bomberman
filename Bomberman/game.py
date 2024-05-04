from dataclasses import field
import gamemap
import gameplayer
import sprites
import keyboard
import utils
import commands

def ComputeMapSpritePosition(DisplaySize, MapSpriteSize):
    (dx, dy) = DisplaySize
    (sx, sy) = MapSpriteSize
    return ((dx - sx) // 2, (dy - sy) // 2)

def GenMapSprite(gmap, images):
    
    d = gmap.data()
    w = gmap.width()
    h = gmap.height()
    fieldsize = images.FieldSize()
    
    MapSprite = sprites.StaticSprite(w*fieldsize, h*fieldsize);    
    MapSprite.pos = ComputeMapSpritePosition()
    MapLine = 0

    for y in range(h):
        for x in range(w):
            sprite = images.GetStaticSprite(d[MapLine + x])
            MapSprite.img.blit(sprite, (x*fieldsize, y*fieldsize))
        MapLine += w
    
    return MapSprite

class Game:    
    
    def __init__(self, cfg, images, keys) -> None:
        self.m_Cfg = cfg
        self.m_Images = images
        self.m_Map = gamemap.Map(cfg["map"])
        self.m_Players = [];
        self.m_Commands = commands.Commands()
        for i,p in enumerate(cfg["players"]):
            self.m_Players.append(self._CreatePlayer(i, p))
        self.m_MapSprite = GenMapSprite(self.m_Map, images)
        self.m_MapSprite.position = ComputeMapSpritePosition(self.m_Cfg["display_size"], self.m_MapSprite.size())
    
    def _CreatePlayer(self, index, cfg) -> gameplayer.Player:
        t = cfg["type"]
        if t != 'key':
            raise utils.Error("Invalid player type: " + t)
        cfg["position"] = self.m_Map.positions()[index]
        p = gameplayer.Player(cfg, self)
        c = keyboard.KeyboardController(cfg["keys"], p)
        p.m_Controller = c
        return p
    
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

    def ToPixelPos(self, pos, origin, fieldsize):
        x = origin[0] + pos[0]*fieldsize//100
        y = origin[1] + pos[1]*fieldsize//100
        return (x, y)    
   
def DrawGame(g, screen):
    MapSprite = g.GetMapSprite()
    screen.blit(MapSprite, MapSprite.GetPosition())
    for p in g.GetPlayers():
        playersprite = p.GetSprite()
        screen.blit(playersprite, g.ToPixelPos(p.Position()))     
    

