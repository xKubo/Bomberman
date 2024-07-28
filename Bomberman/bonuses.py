from configparser import RawConfigParser
from operator import setitem
from random import randint
from screen import Screen
import utils
import random

class BombCfg:
    def __init__(self, bomb_time, flame_size):
        self.m_BombTime = bomb_time
        self.m_FlameSize = flame_size
        
    def BombTime(self):
        return self.m_BombTime
    
    def FlameSize(self):
        return self.m_FlameSize

class PlayerBonuses:
    def __init__(self, cfg):
        self.m_BombCount = cfg["bomb_count"]
        self.m_MaxFlame = cfg["max_flame"]
        self.m_MinFlame = cfg["min_flame"]
        self.m_FlameSize = cfg["flame_size"]
        self.m_BombTime = cfg["bomb_time"]
        self.m_QuickExplodeTime = cfg["quick_explode_time"]
        self.m_Speed = 0
        self.m_DiseaseTime = cfg["disease_time"]
        self.m_SpeedStep = cfg["speed_step"]
        self.m_Step = int(100*cfg["step"])
        self.m_SlowDownStep = int(100*cfg["slowdown_step"])
        self.m_HasMaxFlame = False
        self.m_Times = {
            "min_flame" : 0,
            "slowdown" : 0,
            "reverse" : 0,
            "auto_bomb" : 0,
            "quick_explode" : 0,
            }
        self.m_TimeKeys = list(self.m_Times.keys())
        self.m_Bonuses = []

    def __str__(self):
        diseases = [ (k, v) for k, v in self.m_Times.items() if v > 0]
        return f'BCount={self.m_BombCount}, FS={self.FlameSize()}, Step={self.Step()}, Speed = {self.m_Speed}, SpdStep={self.m_SpeedStep}, D={diseases}'

    def SetSkull(self, times):
        random.shuffle(self.m_TimeKeys)
        for i in range(times):
            self.m_Times[self.m_TimeKeys[i]] = self.m_DiseaseTime
       
    def Update(self, timeinfo):
        self.m_Times = {n:(t-1 if t>=0 else t) for (n,t) in self.m_Times.items()}

    def BombConfiguration(self):
        return BombCfg(self.m_QuickExplodeTime if self.m_Times["quick_explode"] > 0 else self.m_BombTime, self.FlameSize())
    
    def MaxActiveBombCount(self):
        return self.m_BombCount
    
    def AreControlsReversed(self):
        return self.m_Times["reverse"] > 0

    def AutoBomb(self):
        return self.m_Times["auto_bomb"] > 0

    def FlameSize(self):
        if self.m_Times["min_flame"] > 0:
            return self.m_MinFlame
        return self.m_MaxFlame if self.m_HasMaxFlame else self.m_FlameSize

    def IsSkullActive(self):
        return max(self.m_Times) > 0

    def Step(self):
       if self.m_Times["slowdown"] > 0:
           return int(self.m_SlowDownStep)
       return int( self.m_Step  + 100*self.m_SpeedStep*self.m_Speed)
    

class Bonus:
    def __init__(self, name:str, ApplyFn):
        self.m_Name = name
        self.m_Fn = ApplyFn

    def ApplyTo(self, pb:PlayerBonuses):
        self.m_Fn(pb)
    
    def Name(self):
        return self.m_Name    
        

class ArenaBonuses:

    def __init__(self, cfg, sprites):
        self.m_MaxFlame = cfg["defaults"]["max_flame"]
        self.m_Bonuses = [ 
            Bonus('max_flame', lambda pb : setattr(pb, 'm_HasMaxFlame', True)),
            Bonus('flame',     lambda pb : setattr(pb, 'm_FlameSize', pb.m_FlameSize+1)),
            Bonus('bomb',      lambda pb : setattr(pb, 'm_BombCount', pb.m_BombCount+1)),
            Bonus('kick',      lambda pb : setattr(pb, 'm_Kick', True)),
            Bonus('skate',     lambda pb : setattr(pb, 'm_Speed', pb.m_Speed + 1)),
            Bonus('skull',     lambda pb : pb.SetSkull(1)),
            Bonus('max_skull', lambda pb : pb.SetSkull(3)),            
        ]
        for b in self.m_Bonuses:
            b.img = sprites.GetStaticSprite(b.Name())
            
        self.m_PartialSums = []
        val = 0
        for name,o in cfg["occurence"].items():
            val += int(o)
            b = self._FindByName(name)
            self.m_PartialSums.append((val, b))
        self.m_Total = val
        
    def _FindByName(self, name):
        if name == "none":
            return None        
        for b in self.m_Bonuses:
            if b.Name() == name:
                return b
        raise utils.Error("Bonus")


    def GetNextBonus(self) -> Bonus:
        num = randint(0, self.m_Total)
        for n, b in self.m_PartialSums:
            if num < n:
                return b
        return None

    def AddPlayer(self, playerBonuses:PlayerBonuses):
        pass
        
    def Update(self):
        pass
    
