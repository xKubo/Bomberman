
from enum import Enum
from Vec2d import Vector2D
from sprites import Animation

DirToVec = {
    'L' : Vector2D(-1, 0),
    'U' : Vector2D(0, -1),
    'R' : Vector2D(1, 0),
    'D' : Vector2D(0, 1),    
    }

class BombStatus(Enum):
    Ticking = 0,
    Exploding = 1,
    Exploded = 2,

class BombCfg:
    pos = Vector2D(0,0),
    bombTime = 5,
    flameSize = 5,
    flameTime = 5,

class Bomb:
    def __init__(self, bombs, cfg:BombCfg):
        self.m_Position = cfg.pos
        self.m_Timeout = cfg.bombTime
        self.m_ID = id
        self.m_Bombs = bombs
        self.m_Status = BombStatus.Ticking
        self.m_WaitTime = self.m_BombTime
        self.m_Animation = Animation(bombs.GetBombSprites());

    def ID(self):
        return self.m_ID

    def Explode(self) :
        self.m_WaitTime = 0
        self.m_Status =0.
        points = self.m_Bombs.FindFirePoints(self)

    def OnFire(self):
        self.Explode()

    def Update(self):
        if self.m_WaitTime>0:
            self.m_WaitTime =- 1
            self.m_Animation.NextPhase()        
            return True
        if self.m_Status == BombStatus.Ticking:
            self.Explode()
            return True
        if self.m_Status == BombStatus.Exploding:            
            self.m_Status = BombStatus.Exploded
            return False  # can be destroyed

    def Draw(self, scr):
        if self.m_Status == BombStatus.Exploded:
            return;
        if self.m_Status == BombStatus.Ticking:
            scr.DrawSprite(self.m_Animation.GetCurrent(), ToPixelPos(self.m_Position));
    



def PositionToField(pos):
    return Vec2D((pos.x+50)//100, (pos.y+50)//100)
                 
class Map:
    def __init__(self, cfg):
        d = cfg["data"]
        self.m_Height = len(d)
        self.m_Width = len(d[0])
        self.m_Positions = cfg["players"]
        self.m_Data = []
        
        for line in d:
            self.m_Data += line
            
    def IsInMap(self, pt):
        IsXInMap = pt.x >= 0 and pt.x < self.m_Width
        IsYInMap = pt.y >= 0 and pt.y < self.m_Height
        return IsXInMap and IsYInMap

    def ForEachPointInDirDo(self, pos:Vector2D, vec:Vector2D, f):
        while True:
            pos += vec
            if not self.IsInMap(pos):
                return
            if f(pos) == False:
                return

    def width(self):
        return self.m_Width

    def height(self):
        return self.m_Height

    def data(self):
        return self.m_Data

    def dims(self):
        return (self.m_Width, self.m_Height)
    
    def positions(self):
        return self.m_Positions
    
class Bombs:

    def HandleFirePoint(self, pos):
        pt = self.FireObjects(pos)
        if pt == ' ':
            return True;
        if pt == 'W':
            return False;
        if pt == 'w':
            self.SetPt(pos, ' ')
        pass

    def FindFirePoints(self, bomb):
        for dv in DirToVec.values():          
            self.m_Map.ForEachPointInDirDo(bomb.Position(), dv, self.HandleFirePoint)

    BombCounter = 0
    def __init__(self, map:Map, timequeue):
        self.m_Bombs = {}
        self.m_FireCrosses = {}
        self.m_Map = map

    def AddBomb(self, cfg) -> Bomb:        
        Bombs.BombCounter += 1
        BombNum = Bombs.BombCounter

        b = Bomb(self, cfg, BombNum)
        self.m_Bombs[BombNum] = b
        return b

    def RemoveBomb(self, num):
        self.m_Bombs.erase(num)

    def Update(self):
        # update bombs, and destroy bomb if Update return False
        self.m_Bombs = {id:b for id,b in self.m_Bombs.iteritems() if b.Update() == False}

    def Draw(self):
        for b in self.m_Bombs.values():
            b.Draw();
    

