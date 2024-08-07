from enum import Enum
from tkinter.ttk import Separator
from screen import Screen
from sprites import StaticSprite, Animation, Sprites
from gamemap import Map
from Vec2d import Vector2D
from utils import *
from diag import Log
from bonuses import ArenaBonuses,BombCfg



class SearchResult(Enum):
    Continue = 0,
    Stop = 1,

class Bomb:
    
    class Status(Enum):
        Ticking = 0,
        Exploding = 1,
        Exploded = 2,

    def __init__(self, arena, player, cfg:BombCfg, pos:Vector2D, bombid:int, bombAnimation, firecrossAnimation):
        self.m_Player = player
        self.m_Position = pos
        self.m_BombAnimation = bombAnimation
        self.m_CrossAnimation = firecrossAnimation        
        self.m_WaitTime = cfg.BombTime()
        self.m_Cfg = cfg
        self.m_ID = bombid
        self.m_Arena:Arena = arena
        self.m_Status = Bomb.Status.Ticking
        
    def __str__(self):
        return f'B:#={self.m_ID}, Pos={self.m_Position}, WaitTime={self.m_WaitTime}, S={self.m_Status}'

    def Explode(self) :
        if self.m_Status != Bomb.Status.Ticking:
            return
        self.m_Status = Bomb.Status.Exploding
        self.m_WaitTime = self.m_CrossAnimation.TotalTicks()
        Log(f'B:Explode:{id(self)},{self.m_Position}, WT={self.m_WaitTime}')        
        self.BombField().SetType(' ');
        self.m_Fire = self.m_Arena.FindFirePoints(self)
        self.m_Arena.ShowFlames(self.m_Fire)

    def BombField(self):
        return self.m_Arena.GetFieldByPos(self.m_Position)

    def BombFieldPos(self):
        return BestField(self.m_Position)
    
    def OnFire(self):
        self.Explode()

    def Update(self):
        Log(f'B:{id(self)},{self.m_Position}:{self.m_Status}, WT={self.m_WaitTime}')
        if self.m_Status==Bomb.Status.Ticking:
            if self.m_WaitTime>0:
                self.m_WaitTime -= 1
                self.m_BombAnimation.Update()
            else:
                self.Explode()                        
        elif self.m_Status==Bomb.Status.Exploding:
            if self.m_WaitTime>0:
                self.m_WaitTime -= 1
                self.m_CrossAnimation.Update()
            else:
                self.m_Arena.HideFlames(self.m_Fire)
                self.m_Status = Bomb.Status.Exploded
                self.m_Player.OnBombExploded()
        else: 
            pass
  
    def Position(self):
        return self.m_Position
    
    def FlameSize(self):
        return self.m_Cfg.FlameSize()
        
    def Draw(self, scr):
        if self.m_Status==Bomb.Status.Ticking:
            self.m_BombAnimation.Draw(scr, self.m_Position)                     
        elif self.m_Status==Bomb.Status.Exploding:
            self.m_CrossAnimation.Draw(scr, self.m_Fire)
        else: 
            pass        

    def IsDestroyed(self):
        return self.m_Status == Bomb.Status.Exploded

class Wall:
    class Status(Enum):
        Normal = 0,
        Destroying = 1,
        Destroyed = 2,

    def __init__(self, a:Animation, pos:Vector2D, f):
        self.m_Field = f
        self.m_Animation = a
        self.m_Status = Wall.Status.Normal
        self.m_WaitTime = self.m_Animation.TotalTicks()
        self.m_Position = pos
        
    def Update(self):  
        if self.m_Status != Wall.Status.Destroying:
            return
        if self.m_WaitTime >= 0:
            self.m_WaitTime -= 1
            self.m_Animation.Update()
        else:
            self.m_Field.SetType(' ')
            self.m_Status = Wall.Status.Destroyed             

    def Position(self):
        return self.m_Position*100

    def Draw(self, screen:Screen):
        self.m_Animation.Draw(screen, self.m_Position * 100)
    
    def OnFire(self):        
        if self.m_Status != Wall.Status.Normal:
            return
        self.m_Status = Wall.Status.Destroying
    
    def IsDestroyed(self):
        return self.m_Status == Wall.Status.Destroyed 

class Arena:
    
    class NoField:
        def __init__(self, pos):
            self.m_Position = pos

        def __str__(self):
            return f'F:Pos={self.m_Position}, NOFIELD'
    
        def AddObject(self, obj):
            pass
            
        def DelObject(self, obj):
            pass
                
            
        def Type(self):
            return 'W'
        
        def CanVisit(self):
            return False
        
        def Position(self):
            return self.m_Position
        
        def SetType(self, NewType):
            pass

        def SetOnFire(self, OnOff):
            pass
            

    class Field:
        def __init__(self, type, pos):
            self.m_Type = type
            self.m_Objects = []
            self.m_FireCount = 0  
            self.m_Position = pos
            self.m_Bonus = None

        def __str__(self):
            return f'F:Pos={self.m_Position}, F={self.m_FireCount}, T={self.Type()}, CanVisit={self.CanVisit()}'

        def AddObject(self, obj):
            self.m_Objects.append(obj)
            
        def DelObject(self, obj):
            if obj in self.m_Objects:
                self.m_Objects.remove(obj)
            
        def Type(self):
            return 'F' if self.m_FireCount > 0 else self.m_Type
        
        def CanVisit(self):
            return self.m_Type == ' '    
        
        def Position(self):
            return self.m_Position
        
        def GetBonus(self):
            return self.m_Bonus

        def HasBonus(self):
            return self.m_Bonus is not None

        def SetBonus(self, bonus):
            self.m_Bonus = bonus
        
        def SetType(self, NewType):
            self.m_Type = NewType

        def SetOnFire(self, OnOff):
            if OnOff:                
                self.m_FireCount += 1
            else:
                self.m_FireCount -= 1            

    def __init__(self, m:Map, field_tolerance:int, sprites:Sprites, BonusesCfg):
        self.m_Sprites:Sprites = sprites
        self.m_Bombs = []
        self.m_Walls = []
        self.m_Map = m
        self.m_Fields = []        
        self.m_Width = self.m_Map. width()
        self.m_Height = self.m_Map.height()
        self.m_BombCounter = 1
        self.m_Bonuses = ArenaBonuses(BonusesCfg, self.m_Sprites)
        self.m_FieldTolerance = field_tolerance
        d = self.m_Map.data()
        walls = []
        for y in range(self.m_Height):
            for x in range(self.m_Width):
                ch = d[self.m_Width*y + x]
                pos = Vector2D(x,y)
                if ch=='w':
                    walls.append(pos)
                    ch = ' '
                self.m_Fields.append(Arena.Field(ch, pos))
        for wallpos in walls:
            self.AddWall(wallpos)           
        
    def MoveObject(self, obj, OldPos:Vector2D, NewPos:Vector2D):
        fOld = NeighboringFields(OldPos, self.m_FieldTolerance)
        fNew = NeighboringFields(NewPos, self.m_FieldTolerance)
        for fpos in fOld - fNew:
            f = self.GetField(fpos)
            f.DelObject(obj)
        for fpos in fNew - fOld:
            f = self.GetField(fpos)
            f.AddObject(obj)           
            
    def MovePlayer(self, player, OldPos:Vector2D, lastdir, step, keys):
        # find dir that the player will move 
        dir = ComputeNewDir(lastdir, keys, lambda d: CanGo(self, OldPos, DirToVec[d], 100, self.m_FieldTolerance)[2])
        (UpdatedPos, f, cango) = CanGo(self, OldPos, DirToVec[dir], step, self.m_FieldTolerance)
        print(f"M:{OldPos}->{UpdatedPos}: Field:{f}")
        if f.Type() == 'f':
            self.OnFire(player)
        b = f.GetBonus()
        f.SetBonus(None)
        if b is not None:
            b.ApplyTo(player.Bonuses())
        self.MoveObject(player, OldPos, UpdatedPos)
        return (UpdatedPos, dir)
     
    def InArena(self, pos:Vector2D):
        if pos.x < 0 or pos.x >= self.m_Width:
            return False
        if pos.y < 0 or pos.y >= self.m_Height:
            return False
        return True

    def GetExtents(self):
        return (self.m_Width, self.m_Height)
            
    def GetFields(self):
        return self.m_Fields

    def GetField(self, field:Vector2D) -> Field :   
        if not self.InArena(field):
            return Arena.NoField(field)
        return self.m_Fields[field.y*self.m_Width + field.x]
    
    def GetFieldByPos(self, pos:Vector2D) -> Field:
        fp = BestField(pos)
        return self.GetField(fp)
    
    def CanVisit(self, pos:Vector2D, dir:str):
        fp = BestField(pos)
        fp += DirToVec[dir]
        f = self.GetField(fp)
        return f.CanVisit()        
    
    def RegPlayer(self, player, pos:Vector2D):
        self.m_Bonuses.AddPlayer(player)
        fps = NeighboringFields(pos, self.m_FieldTolerance)
        for fp in fps:
            f = self.GetField(fp)
            f.AddObject(player)
    
    def _HandleFirePoint(self, pos):
        f = self.GetField(pos)
        print('FirePoint: ', pos, ' type:', f.Type())                    
        for o in f.m_Objects :
            o.OnFire()
        
        if f.HasBonus():
            if f.Type() == ' ':
                f.SetBonus(None)
            return SearchResult.Stop
        if f.Type() == ' ':
            return SearchResult.Continue
        else:
            return SearchResult.Stop    

    def _FindFirePointsInDir(self, bomb:Bomb, vec:Vector2D, fn):
        counter = 0
        bf = bomb.BombFieldPos()        
        for i in range(1, bomb.FlameSize() + 1) :
            bf += vec
            counter += 1
            field = self.GetField(bf)
            if not self.m_Map.IsInMap(bf):
                print("Not in map", bf)
                return counter
            if fn(bf) == SearchResult.Stop:
                print("Search::stop", bf)
                return counter - 1
        print("Full reached", bf)
        return counter
            
    def FindFirePoints(self, bomb):
        counts = []
        pos = bomb.Position()
        for dv in DirToVec.values():
            cnt = self._FindFirePointsInDir(bomb, dv, self._HandleFirePoint)  
            counts.append(cnt)
        print('FindFire:', bomb.Position(), ' Points: ', counts, " FlameSize: ", bomb.FlameSize())
        for b in self.m_Bombs:
            print(b)
        return {"counts": counts, "pos":bomb.Position(), "size":bomb.FlameSize()}
            
    def _SetFireFields(self, fire, OnOff):
        counts = fire["counts"]
        pos = fire["pos"]
        fpOrig = BestField(pos)
        self.GetField(fpOrig).SetOnFire(OnOff)
        for i, dv in enumerate(DirToVec.values()):            
            for j in range(counts[i]+1):
                fp = fpOrig + dv*j
                self.GetField(fp).SetOnFire(OnOff)
    
    def HideFlames(self, fire):
        self._SetFireFields(fire, False)
        
    def ShowFlames(self, fire):
        self._SetFireFields(fire, True)            

    def AddBomb(self, player, pos, cfg):    
        self.m_BombCounter += 1
        b = Bomb(self, player, cfg, pos, self.m_BombCounter,
                 self.m_Sprites.CreateFieldAnimation('b'), 
                 self.m_Sprites.CreateCrossAnimation())
        print(f'AddBomb:{pos}')
        f = self.GetFieldByPos(b.Position()) 
        if f.Type() != ' ':
            return False    # can add bomb only on free space
        f.SetType('b')
        self.m_Bombs.append(b)
        f.AddObject(b)
        return True
        
    def AddWall(self, pos:Vector2D):
        f = self.GetField(pos)
        f.SetBonus(self.m_Bonuses.GetNextBonus())
        w = Wall(self.m_Sprites.CreateFieldAnimation('w'), pos, f)
        self.m_Walls.append(w);
        
        f.SetType('w')
        f.AddObject(w)
        
    def GetFireCross(self, fire, size):
        return self.m_Sprites.GetFireCross(fire, size)
        
    def _UpdateObjects(self, objs):
        for o in objs:
            o.Update()
            if o.IsDestroyed():
                self.GetFieldByPos(o.Position()).DelObject(o)
        return  [o for o in objs if not o.IsDestroyed()]  

    def Update(self, timeinfo):
        self.m_Bombs = self._UpdateObjects(self.m_Bombs)
        self.m_Walls = self._UpdateObjects(self.m_Walls)

    def Draw(self, scr):
        for w in self.m_Walls:
            w.Draw(scr)        
        for b in self.m_Bombs:
            b.Draw(scr);
        for f in self.m_Fields:
            if f.Type() == ' ' and f.HasBonus():
                scr.DrawSprite(f.GetBonus().img, f.Position()*100)
            
    
