import gamemap
import sprites

def GenMapSprite(gmap, images):
    
    d = gmap.data()
    w = gmap.width()
    h = gmap.height()
    fieldsize = images.FieldSize()
    
    MapSprite = sprites.StaticSprite(w*fieldsize, h*fieldsize);    

    MapLine = 0

    for y in range(h):
        for x in range(w):
            sprite = images.GetStaticSprite(d[MapLine + x])
            MapSprite.img.blit(sprite, (x*fieldsize, y*fieldsize))
        MapLine += w
    
    return MapSprite

class Game:    
    class Cfg:
        w = 320
        h = 240
        
    def __init__(self, cfg, images) -> None:
        self.m_Cfg = cfg
        self.m_Map = gamemap.Map(cfg.map)
        self.m_MapSprite = GenMapSprite(self.m_Map, images)
        pass
    
    def GetMapSprite(self):
        return self.m_MapSprite
    
    def GetCfg(self) -> Cfg:
        return self.m_Cfg
    
    def Update():        
        pass
    
def ComputeCentralRect(DisplaySize, MapSpriteSize):
    (dx, dy) = DisplaySize
    (sx, sy) = MapSpriteSize
    return ((dx - sx) // 2, (dy - sy) // 2)
    

def DrawGame(g, screen):
    MapSprite = g.GetMapSprite()
    screen.blit(MapSprite, ComputeCentralRect(screen.get_size(), MapSprite.rect))
    
