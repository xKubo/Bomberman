from Vec2d import Vector2D

class Error(Exception):
    def __init__(self, message):
        super().__init__(message)
        
DirToVec = {
    'L' : Vector2D(-1, 0),
    'U' : Vector2D(0, -1),
    'R' : Vector2D(1, 0),
    'D' : Vector2D(0, 1),    
    }

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
    return set(map(lambda p: f + Vector2D(p[0]*sign(xOff), p[1]*sign(yOff)), Points))    # adjust for all quadrants

