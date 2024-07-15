class PlayerBonuses:
    def __init__(self, cfg):
        self.m_BombCount = cfg["bomb_count"]
        self.m_FlameSize = cfg["flame_size"]
        self.m_ReversedControls = False    
        self.m_Speed = cfg["speed"]
       
    def Update(self, player):
        pass
    
    def BombCount(self):
        return self.m_BombCount
    
    def FlameSize(self):
        return self.m_FlameSize
    
    def BombTime(self):
        return self.m_BombTime
    
    def AreControlsReversed(self):
        return self.m_ReversedControls
    
    def Speed(self):
        return self.m_Speed

class ArenaBonuses:
    def __init__(self, BonusesCfg):
        self.m_Bonuses = []

    def AddPlayer(self, playerBonuses:PlayerBonuses):
        pass
        
    def Update(self):
        pass
