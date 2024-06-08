
from Vec2d import Vector2D



class Map:
    def __init__(self, cfg):
        d = cfg["data"]
        self.m_Height = len(d)
        self.m_Width = len(d[0])
        self.m_Positions = cfg["players"]
        self.m_Data = []
        
        for line in d:
            self.m_Data += line
            
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




