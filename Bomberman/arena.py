from enum import Enum
from screen import Screen
from sprites import StaticSprite, Animation, Sprites
from gamemap import Map
from Vec2d import Vector2D
from utils import *

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
        self.m_WaitTime = cfg.bombTime
        self.m_Cfg = cfg
        self.m_Arena = arena
        self.m_Status = Bomb.Status.Ticking
        self.m_Animation = Animation(self.m_Arena.GetBombSprites());

    def Explode(self) :
        self.m_WaitTime = self.m_Cfg.flameTime
        self.m_Status = Bomb.Status.Exploding
        self.m_Fire = self.m_Arena.FindFirePoints(self)
        self.m_Arena.ShowFlames(self.m_Fire)
        self.m_Arena.DrawCross(self.m_Fire)

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
        return self.m_Cfg.pos
    
    def FlameSize(self):
        return self.m_Cfg.flameSize
        
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
            if obj in self.m_Objects:
                self.m_Objects.remove(obj)
            
        def Type(self):
            return 'F' if self.m_FireCount > 0 else self.m_Type
        
        def CanVisit(self):
            return self.m_Type == ' '    
        
        def SetOnFire(self, OnOff):
            if OnOff:
                self.m_FireCount += 1
            else:
                self.m_FireCount -= 1            

    def __init__(self, map:Map, field_tolerance, sprites:Sprites):
        self.m_Sprites:Sprites = sprites
        self.m_Bombs = []
        self.m_Walls = []
        self.m_Map = map
        self.m_Fields = []        
        self.m_Width = self.m_Map.width()
        self.m_Height = self.m_Map.height()
        self.m_FieldTolerance = field_tolerance
        for l in self.m_Map.data():
            for ch in l:
                self.m_Fields.append(Arena.Field(ch))

    def DelObject(self, obj, field):
        self.GetField(field).DelObject(obj)
        
    def AddObject(self, obj, field):
        self.GetField(field).AddObject(obj)
        
    def MoveObject(self, obj, OldPos:Vector2D, NewPos:Vector2D):
        fOld = NeighboringFields(OldPos, self.m_FieldTolerance)
        fNew = NeighboringFields(NewPos, self.m_FieldTolerance)
        for f in fOld - fNew:
            self.DelObject(obj, f)
        for f in fNew - fOld:
            self.AddObject(obj, f)   
            
    def _CanGo(self, OldPos:Vector2D, NewPos:Vector2D):
        fpOld = BestField(OldPos)
        fpNew = BestField(NewPos)
        f = self.GetField(fpNew) 
        if fpOld == fpNew:
            return (NewPos, f)                   
        return (NewPos if f.CanVisit() else FieldBoundary(OldPos, NewPos), f)
            
    def MovePlayer(self, player, OldPos:Vector2D, NewPos:Vector2D):
        (UpdatedPos, field) = self._CanGo(OldPos, NewPos)
        if field.Type() == 'f':
            self.OnFire(player)
        self.MoveObject(player, OldPos, UpdatedPos)
        return UpdatedPos
            
    def GetField(self, field:Vector2D) -> Field :
        return self.m_Fields[field.y*self.m_Width + field.x]
    
    def GetFieldByPos(self, pos:Vector2D) -> Field:
        fp = BestField(pos)
        return self.GetField(fp)
    
    def CanVisit(self, pos:Vector2D, dir):
        fp = self.GetFieldByPos(pos)
        fp += dir
        f = self.GetField(fp)
        return f.IsFree()        
    
    def RegPlayer(self, player, pos:Vector2D):
        self.MovePlayer(player, pos, pos)
    
    def _HandleFirePoint(self, pos):
        f = self.GetFieldAt(pos)
                    
        for o in f.objects :
            o.OnFire()
            
        pt = f.type
        if pt == ' ':
            return SearchResult.Continue
        else:
            return SearchResult.Stop    

    def _FindFirePointsInDir(self, bomb:Bomb, vec:Vector2D, fn):
        counter = 0
        pos = bomb.Position()
        for i in range(bomb.FlameSize()) :
            pos += vec
            ++counter
            field = self.GetField(pos)
            if not self.m_Map.IsInMap(pos):
                return counter - 1
            if fn(pos) == SearchResult.Stop:
                return counter - 1
            
    def FindFirePoints(self, bomb):
        counts = []
        pos = bomb.Position()
        for dv in DirToVec.values():
            cnt = self._FindFirePointsInDir(bomb, dv, self._HandleFirePoint)  
            counts.append(cnt)
        return {"counts": counts, "pos":bomb.Position()}
            
    def SetFireFields(self, fire, OnOff):
        counts = fire["counts"]
        pos = fire["pos"]
        fpOrig = BestField(pos)
        self.GetField(fpOrig).SetOnFire(OnOff)
        for i, dv in enumerate(DirToVec.values()):            
            for j in range(counts[i]):
                fp = fpOrig + dv*j
                self.GetField(fp).SetOnFire(OnOff)
    
    def HideFlames(self, fire):
        self._SetFireFields(self, fire, 1)
        
    def ShowFlames(self, fire):
        self._SetFireFields(self, fire, 0)            

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
    
    def GetBombSprites(self):
        self.m_Sprites.GetAnimation('b')
        
    def GetFireCross(self, fire, size):
        return self.m_Sprites.GetFireCross(fire, size)
        
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
        
    
