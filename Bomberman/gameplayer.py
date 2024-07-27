import copy
from enum import Enum
import sprites
from bonuses import PlayerBonuses
from Vec2d import Vector2D

from utils import BestField, DirToVec, MiddleOfTheField
from arena import Arena, BombCfg, EmptyDir, Dirs

class Player:      
            
    class Status(Enum):
        Normal = 0,
        Dying = 1,
        Dead = 2,

    def __init__(self, cfg, game) -> None:
        self.m_Direction = 'R'
        self.m_Sprites = {}
        self.m_Cfg = cfg
        self.m_ActiveBombCount = 0
        p = self.m_Cfg["position"]
        self.m_Position = Vector2D(*p) * 100 + MiddleOfTheField
        self.m_Bonuses = PlayerBonuses(self.m_Cfg["bonuses"])
        self.m_Game = game
        self.m_Status:Player.Status = Player.Status.Normal
        self.m_Name = self.m_Cfg["name"]
        self.m_Arena: Arena = game.Arena()
        self.m_Arena.RegPlayer(self, self.m_Position)
        self.m_CurrentKeys = ""
        self.m_DeadAnimation = self.m_Game.GetAnimation('X')
        self.m_WaitTime = self.m_DeadAnimation.TotalTicks()
        for d in DirToVec.keys():
            self.m_Sprites[d] = self.m_Game.GetAnimation(d)
         
    def GetStatus(self):
        return self.m_Status

    def Name(self):
        return self.m_Name
        
    def Direction(self):
        return self.m_Direction

    def Position(self):
        return self.m_Position

    def Move(self):
        if self.m_Status != Player.Status.Normal:
            return;
        self.m_Sprites[self.m_Direction].Update()
        (self.m_Position, self.m_Direction) = self.m_Arena.MovePlayer(self, self.m_Position, self.m_Direction, self.m_Bonuses.Step(), self.m_CurrentKeys)
           
    def OnFire(self):
         if self.m_Status == Player.Status.Normal:
            self.m_Status = Player.Status.Dying   

    def DeployBomb(self):
        if self.m_Status != Player.Status.Normal:
            return;
        pos = self.Position()
        pos = BestField(pos)*100
        if (self.m_ActiveBombCount < self.m_Bonuses.MaxActiveBombCount()):
            self.m_ActiveBombCount += 1
            self.m_Arena.AddBomb(self, pos, self.m_Bonuses.BombConfiguration())        

    def OnBombExploded(self):
        self.m_ActiveBombCount -= 1

    def OnCmd(self, cmd):
        if cmd!= self.m_CurrentKeys:
            if 'B' in cmd and not 'B' in self.m_CurrentKeys:
                self.m_CurrentKeys = cmd
                self.DeployBomb()
                return
            self.m_CurrentKeys = cmd
         

    def Update(self):
        if self.m_Status == Player.Status.Dead:
            return
        if self.m_Status == Player.Status.Dying:
            if self.m_WaitTime == 0:
                self.m_Status = Player.Status.Dead;
                self.m_Status = Player.Status.Normal;
                self.m_WaitTime = self.m_DeadAnimation.TotalTicks()
            self.m_WaitTime -= 1
            self.m_DeadAnimation.Update()
            return
        if self.m_Status == Player.Status.Normal:
            if self.m_CurrentKeys not in ["", "B"]:            
                self.Move()
                
    def Bonuses(self):
        return self.m_Bonuses
            
    def Draw(self, scr):
        if self.m_Status == Player.Status.Dead:
            return   
        if self.m_Status == Player.Status.Dying:
            self.m_DeadAnimation.Draw(scr, self.Position() - MiddleOfTheField)
            return
        self.m_Sprites[self.m_Direction].Draw(scr, self.Position() - MiddleOfTheField)
        
       
    
        
