
from Vec2d import Vector2D

DirToVec = {
    'L' : Vector2D(-1, 0),
    'U' : Vector2D(0, -1),
    'R' : Vector2D(1, 0),
    'D' : Vector2D(0, 1),    
    }

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

    def ForEachPointInDirDo(self, pos:Vector2D, vec:Vector2D, f):
        while True:
            pos += vec
            if not self.IsInMap(pos):
                return
            if f(pos) == False:
                return

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




#pick one field from 4 possible ones           
def BestField(posUpperLeft:Vector2D):
    return Vector2D((posUpperLeft.x+50)//100, (posUpperLeft.y+50)//100)
    
Table = [
    [(0,0)],
    [(0,0), (0,1)],
    [(0,0), (1,0)],
    [(0,0), (1,0), (0,1), (1,1)],
]

def sign(x):
    return 1 if x>=0 else -1

# return neighboring fields
def NeighboringFields(posUpperLeft:Vector2D, tolerance:int):
    pos = Vector2D(posUpperLeft.x + 50, posUpperLeft.y + 50)  # position of the center 
    f = BestField(posUpperLeft)
    xOff = pos.x%100 - 50   # distance from center point
    yOff = pos.y%100 - 50
    xAbs = abs(xOff) > tolerance  # is within tolerance? 
    yAbs = abs(yOff) > tolerance  
    Points = Table[xAbs + 2*yAbs]    # return 1, 2, or 4 points
    return list(map(lambda p: f + Vector2D(p[0]*sign(xOff), p[1]*sign(yOff)), Points))    # adjust for all quadrants
    

