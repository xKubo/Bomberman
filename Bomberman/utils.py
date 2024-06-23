from Vec2d import Vector2D, Error

        
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

def FieldBoundary(OldPos:Vector2D, NewPos:Vector2D):
    d = NewPos - OldPos

    for i in range(2):
        q = OldPos[i]//100
        if d[i] > 0:
            NewPos[i] = q*100 + 99
        elif d[i] < 0:
            NewPos[i] = q*100
    return NewPos

def ParseTimeToMS(TimeStr:str):
    if TimeStr.endswith('ms'):
        ms = int(TimeStr[:-2])
        return ms
    if TimeStr.endswith('s'):
        s = int(TimeStr[:-1])
        return s*1000
    
def ParseTimeLineCfg(cfg):
    type = cfg["type"]
    res = {}
    match type:
        case "normal":
            res["frames"] = []
        case "custom":
            frames = []
            for c in cfg["timeline"]:
                num = ord(c) - ord('0')
                frames.append(num)
            res["frames"] = frames
        case _ : 
            raise Error("Invalid timeline type:" + type)
    res["frame_time"] = ParseTimeToMS(cfg["time"])
    return res;