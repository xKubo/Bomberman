import string
import sprites
import commands

class Position:
    pass

DirsToVec = {
    'l' : (-1, 0),
    'r' : (1, 0),
    'u' : (0, -1),
    'd' : (0, 1),    
    }

def DirToPos(dir, step):
    (x, y) = DirsToVec[dir]
    return (x*step, y*step)
    

class Player:
    class Cfg:
        step = 4,
        speed = 100,
        position:Position
        name:string = ''
        

    def __init__(self, cfg:Cfg, controller, commands:commands.Commands, images:sprites.Sprites) -> None:
        self.m_Controller = controller
        self.m_Direction = 'R'
        self.m_Sprites = {}
        self.m_Commands = commands
        self.m_Cfg = cfg
        self.m_Position = self.m_Cfg.position
        for d in "LURD":
            self.sprites[d] = images.GetAnimation(d)
        
    def Direction(self):
        return self.m_Direction

    def CanGo(dir):
        return True # zatial nekontrolujem

    def MoveTo(self, dir):
        self.m_Commands.AddCmd("P" + self.m_Cfg.name + ":" + dir)
        if self.CanGo(dir):
            self.m_Position += DirToPos(dir, self.m_Cfg.step)

    def Update(self):
        self.m_Controller.Update()

        

def DrawPlayer(player, screen):
    pass
    
        
