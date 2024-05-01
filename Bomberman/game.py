

class Game:    
    class Cfg:
        w = 320
        h = 240
        
    def __init__(self, cfg) -> None:
        self.m_Cfg = cfg
        pass
    
    def GetCfg(self) -> Cfg:
        return self.m_Cfg
    


