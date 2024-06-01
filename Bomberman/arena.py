
from ast import Continue
import math
from enum import Enum
from pickletools import read_stringnl_noescape_pair

from sprites import StaticSprite, Animation, Sprites
from gamemap import DirToVec, Map
from Vec2d import Vector2D

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
    def __init__(self, fields, cfg:BombCfg):
        self.m_Position = cfg.pos
        self.m_Timeout = cfg.bombTime
        self.m_ID = id
        self.m_Fields = fields
        self.m_Status = BombStatus.Ticking
        self.m_WaitTime = self.m_BombTime
        self.m_Animation = Animation(fields.GetBombSprites());

    def ID(self):
        return self.m_ID

    def Explode(self) :
        self.m_WaitTime = 0
        self.m_Status =0.
        points = self.m_Fields.FindFirePoints(self)

    def OnFire(self):
        self.Explode()

    def Update(self) -> BombStatus:
        if self.m_WaitTime>0:
            self.m_WaitTime =- 1
            self.m_Animation.NextPhase()        
            return self.m_Status
        if self.m_Status == BombStatus.Ticking:
            self.Explode()
            return self.m_Status
        if self.m_Status == BombStatus.Exploding:            
            self.m_Status = BombStatus.Exploded
        return self.m_Status  # can be destroyed

    def Draw(self, scr):
        if self.m_Status == BombStatus.Exploded:
            return;
        if self.m_Status == BombStatus.Ticking:
            scr.DrawSprite(self.m_Animation.GetCurrent(), scr.ToPixelPos(self.m_Position));

class Wall:
    def __init__(self, animation:Animation):
        self.m_Animation = animation
        
    def Update(self):
        pass
    
    def Draw(self):
        pass
    
    def OnFire(self):
        pass

class Arena:

    class Field:
        def __init__(self, type):
            self.m_Type = type
            

    def __init__(self, map:Map):
        self.m_Bombs = {}
        self.m_Walls = []
        self.m_Map = map
        self.m_Fields = []
        
    def MoveObject(obj, OldPos:Vector2D, NewPos:Vector2D):
        pass
    
    def AddBomb(self, cfg:BombCfg):
        pass
    
    def AddWall(self, pos:Vector2D):
        self.m_Walls.append(Wall(pos));
    
    def RegPlayer(self, pos:Vector2D, player):
        pass
    
    def HandleFirePoint(self, pos):
        f = self.GetFieldAt(pos)
                    
        for o in f.objects :
            o.OnFire()
            
        pt = f.type
        if pt == ' ':
            return Continue
        else:
            return Stop    

    Ohen musi nastavit typ pola na f - aby ak ho trafi hrac, aby zahynul

    def FindFirePoints(self, bomb):
        for dv in DirToVec.values():          
            self.m_Map.ForEachPointInDirDo(bomb.Position(), dv, self.HandleFirePoint)        

    def AddBomb(self, cfg) -> Bomb:        
        b = Bomb(self, cfg, BombNum)
        self.m_Bombs[BombNum] = b
        return b

    def Update(self):
        # update bombs keep only non-exploded bombs
        self.m_Walls = 
        self.m_Bombs = {id:b for id,b in self.m_Bombs.iteritems() if b.Update() != BombStatus.Exploded}

    def Draw(self):
        for b in self.m_Bombs.values():
            b.Draw();
    
