import utils
import string
import sprites
import commands

class Position:
    pass

DirsToVec = {
    'L' : (-1, 0),
    'R' : (1, 0),
    'U' : (0, -1),
    'D' : (0, 1),    
    }

def DirToPos(dir, step):
    (x, y) = DirsToVec[dir]
    return (x*step, y*step)
    

class Player:      
    def __init__(self, cfg, game) -> None:
        self.m_Direction = 'R'
        self.m_Sprites = {}
        self.m_Cfg = cfg
        self.m_Position = self.m_Cfg["position"]
        self.m_Game = game
        for d in DirsToVec.keys():
            self.m_Sprites[d] = self.m_Game.GetAnimation(d)
        
    def GetDirection(self):
        return self.m_Direction

    def GetPosition(self):
        return self.m_Position

    def CanGo(dir):
        return True # zatial nekontrolujem

    def MoveTo(self, dir):
        self.m_Game.AddCmd("P" + self.m_Cfg.name + ":" + dir)
        if self.CanGo(dir):
            self.m_Position += DirToPos(dir, self.m_Cfg.step)
           
    def OnCmd(self, cmd):
        if cmd in DirsToVec.keys:
            self.MoveTo(self, dir)
        else:
            raise utils.Error("Invalid cmd: " + cmd)            

    def Update(self):
        self.m_Controller.Update()

    def GetSprite(self):
        return self.m_Sprites[self.m_Direction].GetNext()
        
        

       
    
        
