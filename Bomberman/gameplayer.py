import utils
import sprites
from Vec2d import Vector2D

from utils import DirToVec
from arena import Arena, BombCfg

EmptyDir = ' '
Dirs = 'LURD'

def OppositeDirs(Dir):
    index = Dirs.index(Dir)
    return (Dirs[(index+1)%4], Dirs[(index+3)%4])

def ComputeNewDir(LastDir, NewChars, CanGo):
    if NewChars=='':
        return LastDir
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
        self.m_Position = Vector2D(*p) * 100
        self.m_Step = int(self.m_Cfg["step"] * 100)
        self.m_Game = game
        self.m_Arena: Arena = game.Arena() 
        self.m_Arena.RegPlayer(self, p)
        self.m_CurrentKeys = ""
        self.m_BombCfg = BombCfg()
        for d in DirToVec.keys():
            self.m_Sprites[d] = self.m_Game.GetAnimation(d)
        
    def GetDirection(self):
        return self.m_Direction

    def GetPosition(self):
        return self.m_Position

    def MoveTo(self, dir):
        self.m_Game.AddCmd("P" + self.m_Cfg["name"] + ":" + dir)
        self.m_Sprites[self.m_Direction].NextPhase()
        NewPos = self.m_Position + DirToVec[dir] * self.m_Step
        self.m_Position = self.m_Arena.MovePlayer(self.m_Position, NewPos)
           
    def OnCmd(self, cmd):
        if cmd!= self.m_CurrentKeys:
            if 'B' in cmd and not 'B' in self.m_CurrentKeys:
                self.m_BombCfg.pos = self.GetPosition()
                self.m_Arena.AddBomb(self.m_BombCfg)
            self.m_CurrentKeys = cmd
            print(f'{cmd}:{self.m_Position}')            
            self.m_Direction = ComputeNewDir(self.m_Direction, cmd, self.CanGo)            

    def Update(self):
        if self.m_CurrentKeys != "":
            self.MoveTo(self.m_Direction)
            
    def Draw(self, scr):
        return self.m_Sprites[self.m_Direction].GetCurrent()
        
    def DeployBomb(self):
        self.m_BombCfg.pos = self.GetPosition()
        self.m_Arena.DeployBomb(self.m_BombCfg)

       
    
        
