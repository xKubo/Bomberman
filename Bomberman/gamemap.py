

class Map:
    class Cfg:
        w = 0
        h = 0
        data = []


    def __init__(self, cfg):
        self._cfg = cfg
        self._GenImg()
        
    def GetCfg(self):
        return self._cfg



    def dims(self):
        return (self.cfg.w, self.cfg.h)
    
    def GetImage(self):
        pass
    

