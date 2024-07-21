from screen import Screen

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
        self.m_FlameSize = cfg["flame_size"]
        self.m_BombTime = cfg["bomb_time"]
        self.m_ReversedControls = False
        self.m_Speed = cfg["speed"]
        self.m_Step = cfg["step"]
       
    def Update(self, player):
        pass    

    def BombConfiguration(self):
        return BombCfg(self.m_BombTime, self.m_FlameSize)
    
    def MaxActiveBombCount(self):
        return self.m_BombCount
    
    def AreControlsReversed(self):
        return self.m_ReversedControls
    
    def Speed(self):
        return self.m_Speed

    def Step(self):
        return self.m_Step
    

class Bonus:
    def __init__(self, name:str, ApplyFn):
        self.m_Name = name
        self.m_Fn = ApplyFn

    def ApplyTo(self, pb:PlayerBonuses):
        self.m_Fn(pb)
    
    def Name(self):
        return self.m_Name    
        
class ArenaBonuses:
    def __init__(self, BonusesCfg, sprites):
        
        self.m_Bonuses = []

    def _CreateBonus(cfg, sprites):
        pass

    def AddPlayer(self, playerBonuses:PlayerBonuses):
        pass
    
    def GenerateBonuses(map):
        pass
        
    def Update(self):
        pass
    
    def Draw(self, scr):
        pass
