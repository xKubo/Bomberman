import utils
import sprites
from Vec2d import Vector2D

DirToVec = {
    'L' : Vector2D(-1, 0),
    'U' : Vector2D(0, -1),
    'R' : Vector2D(1, 0),
    'D' : Vector2D(0, 1),    
    }


EmptyDir = ' '
Dirs = 'LURD'

def OppositeDirs(Dir):
    index = Dirs.index(Dir)
    return (Dirs[(index+1)%4], Dirs[(index-1)%4])

def ComputeNewDir(LastDir, NewChars, CanGo):
    if NewChars=='':
        return EmptyDir
    CurrDir = NewChars[0]
    if LastDir == EmptyDir:
        return CurrDir
    if LastDir not in NewChars:
        return CurrDir
    opp = OppositeDirs(LastDir)
    for o in opp:
        if o in NewChars and CanGo(o):
            return o
    return LastDir

class Player:      
    def __init__(self, cfg, game) -> None:
        self.m_Direction = 'R'
        self.m_Sprites = {}
        self.m_Cfg = cfg
        p = self.m_Cfg["position"]
        self.m_Position = Vector2D.from_tuple(p)
        self.m_Step = self.m_Cfg["step"]
        self.m_Game = game
        self.m_CurrentKeys = ""
        for d in DirToVec.keys():
            self.m_Sprites[d] = self.m_Game.GetAnimation(d)
        
    def GetDirection(self):
        return self.m_Direction

    def GetPosition(self):
        return self.m_Position

    def CanGo(self, dir):
        return True # zatial nekontrolujem

    def MoveTo(self, dir):
        self.m_Game.AddCmd("P" + self.m_Cfg["name"] + ":" + dir)
        self.m_Sprites[self.m_Direction].NextPhase()
        if self.CanGo(dir):
            self.m_Position += DirToVec[dir] * self.m_Step
           
    def OnCmd(self, cmd):
        if cmd!= self.m_CurrentKeys:
            self.m_CurrentKeys = cmd
            print(f'{cmd}:{self.m_Position}')
            self.m_Direction = ComputeNewDir(self.m_Direction, cmd, self.CanGo)
            

    def Update(self):
        if self.m_CurrentKeys != "":
            self.MoveTo(self.m_CurrentKeys)

    def GetSprite(self):
        return self.m_Sprites[self.m_Direction].GetCurrent()
        
        

       
    
        
