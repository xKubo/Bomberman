

class Map:
    class Cfg:
        w = 0
        h = 0
        data = ""
        player_positions = [(20, 20), (10, 10)] 


    def __init__(self, cfg:Cfg):
        self._cfg = cfg
        self._GenImg()
        
    def GetCfg(self):
        return self._cfg



    def dims(self):
        return (self.cfg.w, self.cfg.h)
    
    def GetImage(self):
        pass
    

