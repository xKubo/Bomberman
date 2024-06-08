from enum import Enum
from screen import Screen
from sprites import StaticSprite, Animation, Sprites
from gamemap import Map
from Vec2d import Vector2D
from utils import DirToVec, BestField, NeighboringFields

class BombCfg:
    pos = Vector2D(0,0),
    bombTime = 5,
    flameSize = 5,
    flameTime = 5,

class SearchResult(Enum):
    Continue = 0,
    Stop = 1,

class Bomb:
    
    class Status(Enum):
        Ticking = 0,
        Exploding = 1,
        Exploded = 2,

    def __init__(self, arena, cfg:BombCfg):
        self.m_Position = cfg.pos
        self.m_Timeout = cfg.bombTime
        self.m_Cfg = cfg
        self.m_ID = id
        self.m_Arena = arena
        self.m_Status = Bomb.Status.Ticking
        self.m_WaitTime = self.m_BombTime
        self.m_Animation = Animation(self.m_Arena.GetBombSprites());

    def ID(self):
        return self.m_ID

    def Explode(self) :
        self.m_WaitTime = self.m_Cfg.flameTime
        self.m_Status = Bomb.Status.Exploding
        self.m_Fire = self.m_Arena.FindFirePoints(self)
        self.m_Arena.DrawFire(self.m_Fire)

    def OnFire(self):
        self.Explode()

    def Update(self):
        match self.m_Status:
            case Bomb.Status.Ticking:
                if self.m_WaitTime>0:
                    self.m_WaitTime =- 1
                    self.m_Animation.NextPhase()
                else:
                    self.Explode(self)                        
            case Bomb.Status.Exploding:            
                if self.m_WaitTime>0:
                    self.m_WaitTime =- 1
                else:
                    self.m_Arena.HideFlames(self.m_Fire)
                    self.m_Status = Bomb.Status.Exploded
            case Bomb.Status.Exploded:
                pass
            
    def Position(self):
        return Vector2D(*self.m_Cfg.pos)
        
    def Draw(self, scr):
        match self.m_Status:
            case Bomb.Status.Ticking:
                scr.DrawSprite(self.m_Animation.GetCurrent(), self.m_Position);
            case Bomb.Status.Exploding:
                self.m_Arena.DrawFire(self.m_Fire)
            case Bomb.Status.Exploded:
                pass            

    def IsDestroyed(self):
        return self.m_Status == Bomb.Status.Exploded

class Wall:
    class Status(Enum):
        Normal = 0,
        Destroying = 1,
        Destroyed = 2,

    def __init__(self, sprites:Sprites, pos:Vector2D):
        self.m_Animation = Animation(sprites)
        self.m_Status = Wall.Status.Normal
        self.m_Frame = self.m_Animation.size()
        self.m_Position = pos
        
    def Update(self):   
        if self.m_Status != Wall.Status.Destroying:
            return
        if self.m_Frame >= 0:
            self.m_Frame -= 1
            self.m_Animation.NextPhase()
        else:
            self.m_Status = Wall.Status.Destroyed             

    def Draw(self, screen:Screen):
        screen.DrawSprite(self.m_Animation.GetCurrent(), self.m_Position)
    
    def OnFire(self):        
        if self.m_Status != Wall.Status.Normal:
            return
        self.m_Status = Wall.Status.Destroying
    
    def IsDestroyed(self):
        return self.m_Status == Wall.Status.Destroyed 

class Arena:

    class Field:
        def __init__(self, type):
            self.m_Type = type
            self.m_Objects = []
            self.m_FireCount = 0          

        def AddObject(self, obj):
            self.m_Objects.append(obj)
            
        def DelObject(self, obj):
            self.m_Objects.remove(obj)
            

    def __init__(self, map:Map):
        self.m_Bombs = []
        self.m_Walls = []
        self.m_Map = map
        self.m_Fields = []        
        self.m_Width = self.m_Map.width()
        self.m_Height = self.m_Map.height()
        for l in self.m_Map.data():
            for ch in l:
                self.m_Fields.append(Arena.Field(ch))
        
    def MoveObject(self, obj, OldPos:Vector2D, NewPos:Vector2D):
        fOld = NeighboringFields(OldPos)
        fNew = NeighboringFields(NewPos)
        for f in fOld - fNew:
            self.DelObject(obj, f)
        for f in fNew - fOld:
            self.AddObject(obj, f)   
            
    def _CanGo(self, OldPos:Vector2D, NewPos:Vector2D):
        fOld = BestField(OldPos)
        fNew = BestField(NewPos)
        if fOld == fNew:
            return NewPos
        f = self.GetField(fNew)
        return NewPos if f.Type() == ' ' else OldPos  #toto treba upravit, treba najst hranicu policka
            
    def MovePlayer(self, OldPos:Vector2D, NewPos:Vector2D):
        UpdatedPos = self._CanGo(OldPos, NewPos)
        self.MoveObject(self, OldPos, UpdatedPos)
            
    def GetField(self, field:Vector2D) -> Field :
        return self.m_Fields[field.y*self.m_Width + field.x]
    
    def GetFieldByPos(self, pos:Vector2D) -> Field:
        fp = BestField(pos)
        return self.GetField(fp)
    
    def RegPlayer(self, pos:Vector2D, player):
        pass
    
    def _HandleFirePoint(self, pos):
        f = self.GetFieldAt(pos)
                    
        for o in f.objects :
            o.OnFire()
            
        pt = f.type
        if pt == ' ':
            return SearchResult.Continue
        else:
            return SearchResult.Stop    

    def FindFirePoints(self, bomb):
        points = []
        for dv in DirToVec.values():          
            pt = self.ForEachPointInDirDo(bomb.Position(), dv, self._HandleFirePoint)  
            points.append(pt)
        return points
            
    def ForEachPointInDirDo(self, pos:Vector2D, vec:Vector2D, fn):
        while True:
            pos += vec
            field = self.GetField(pos)
            if not self.m_Map.IsInMap(pos):
                return pos - vec
            if fn(pos) == SearchResult.Stop:
                return pos - vec

    def AddBomb(self, cfg):        
        b = Bomb(self, cfg)
        pos = b.Position()
        f = self.GetFieldByPos(b.Position()) 
        if f.Type() != ' ':
            return      # can add bomb only on free space
        self.m_Bombs.append(b)
        f.AddObject(b)
        
    def AddWall(self, pos:Vector2D):
        self.m_Walls.append(Wall(pos));
    
    def DrawFire(self, fire):
        pass
    
    def HideFire(self, fire):
        pass
        
    def _UpdateObjects(self, objs):
        for o in objs:
            o.Update()
            if o.IsDestroyed():
                self.GetFieldByPos(o.Position()).DelObject(o)
        return  [o for o in objs if not o.IsDestroyed()]  

    def Update(self):
        self._UpdateObjects(self.m_Bombs)
        self._UpdateObjects(self.m_Walls)

    def Draw(self, scr):
        for w in self.m_Walls:
            w.Draw(scr)        
        for b in self.m_Bombs:
            b.Draw(scr);
        
    
