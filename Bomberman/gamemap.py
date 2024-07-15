
from Vec2d import Vector2D
import random

from utils import DirToVec


class Map:
    def __init__(self, cfg):
        d = cfg["data"]
        self.m_Height = len(d)
        self.m_Width = len(d[0])
        self.m_Positions = cfg["players"]
        self.m_Pillars = cfg["pillars"]
        self.m_Data = []
        
        for line in d:
            self.m_Data += line

        if cfg["pillars"]:
            for y in range(2, self.m_Height-2, 2):
                for x in range(2, self.m_Width-2, 2):
                    self.m_Data[y*self.m_Width + x] = 'W'                

        self._GenRandomWalls(cfg["random_walls"])    
        
        for p in self.m_Positions:
            pv = Vector2D(*p)

            fields = self._FieldsNearPlayer(pv)
            for f in fields:                
                idx = f[0] + self.m_Width*f[1]
                if self.m_Data[idx] == 'w':
                    self.m_Data[idx] = ' '                

    def _FieldsNearPlayer(self, p:Vector2D):
        res = [p]
        for dv in DirToVec.values():
            res.append(p + dv)
        return res
    
    def _GenRandomWall(d, skip:int):
        if d == 'n':
            return ' '
        if d!=' ':
            return d
        pass

    def _GenRandomWalls(self, skip:int):
        if skip == 0:
            self.m_Data = list(map(lambda f: ' ' if f == 'n' else f, self.m_Data))
            return
        r = random.randint(0, skip)
      #  NewData = list(map(lambda f: self._GenRandomWall(f, skip)))
        for i,d in enumerate(self.m_Data):
            if d != ' ':
                if d == 'n':
                    self.m_Data[i] = ' '
                continue
            if r == 0:
                r = random.randint(0, skip)
            else:
                r -= 1
                self.m_Data[i] = 'w'
                
            
    def IsInMap(self, pt):
        IsXInMap = pt.x >= 0 and pt.x < self.m_Width
        IsYInMap = pt.y >= 0 and pt.y < self.m_Height
        return IsXInMap and IsYInMap

    def width(self):
        return self.m_Width

    def height(self):
        return self.m_Height

    def data(self):
        return self.m_Data

    def dims(self):
        return (self.m_Width, self.m_Height)
    
    def positions(self):
        return self.m_Positions




