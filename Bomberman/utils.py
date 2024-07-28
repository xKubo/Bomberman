from Vec2d import Vector2D, Error

        
DirToVec = {
    'L' : Vector2D(-1, 0),
    'U' : Vector2D(0, -1),
    'R' : Vector2D(1, 0),
    'D' : Vector2D(0, 1),    
    }


MiddleOfTheField = Vector2D(50, 50)

#pick one field from 4 possible ones           
def BestField(posUpperLeft:Vector2D):
    return Vector2D(posUpperLeft.x//100, posUpperLeft.y//100)
    
Table = [
    [(0,0)],
    [(0,0), (0,1)],
    [(0,0), (1,0)],
    [(0,0), (1,0), (0,1), (1,1)],
]

def sign(x):
    return 1 if x>=0 else -1


# return neighboring fields
def NeighboringFields(pos:Vector2D, tolerance:int) -> set: 
    f = BestField(pos)
    xOff = pos.x%100 - 50   # distance from center point
    yOff = pos.y%100 - 50
    xAbs = abs(xOff) > tolerance  # is within tolerance? 
    yAbs = abs(yOff) > tolerance  
    Points = Table[xAbs + 2*yAbs]    # return 1, 2, or 4 points
    return set(map(lambda p: f + Vector2D(p[0]*sign(xOff), p[1]*sign(yOff)), Points))    # adjust for all quadrants



def FieldsInDirection(pos:Vector2D, dv:Vector2D, field_tolerance:int):
    if dv.x == 0:       
        n = Vector2D(1,0)
    else:
        n = Vector2D(0,1)
    f = BestField(pos)
    m = f * 100 + MiddleOfTheField  #middlepoint
    dist = pos[n[1]]-m[n[1]]
    res = f + dv
    if abs(dist) < field_tolerance:
        return [res]
    else:
        return [res, res+n if dist>0 else res-n]            

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
    if type=="normal":
        res["frames"] = []
    elif type=="custom":
        frames = []
        for c in cfg["timeline"]:
            num = ord(c) - ord('0')
            frames.append(num)
        res["frames"] = frames
    else: 
        raise Error("Invalid timeline type:" + type)
    res["frame_time"] = ParseTimeToMS(cfg["time"])
    return res;

def UpdateTimeToTicks(cfg, Keys, TickMS:int):
    for k in Keys:
        cfg[k] = ParseTimeToMS(cfg[k])//TickMS;


def CanGo(fields, OldPos:Vector2D, dir:Vector2D, step:int, FieldTolerance:int):
    NewPos = OldPos + dir*step
    fNew = fields.GetFieldByPos(NewPos) 
    fOld = fields.GetFieldByPos(OldPos) 
    middle = OldPos//100*100 + MiddleOfTheField
    posvec = NewPos - middle
    if posvec.dot(dir) < FieldTolerance:
        return (NewPos, fNew, True)    
    fieldposes = FieldsInDirection(OldPos, dir, FieldTolerance)        
    CanVisitAll = min(map(lambda fpos:fields.GetField(fpos).CanVisit(), fieldposes))
    
    CanVisitResult = (NewPos, fNew, True)
    CannotVisitResult = (middle + dir*FieldTolerance, fOld, False)
    print(f"D:{dir}, O:{OldPos}, N:{NewPos}, FPos:{fieldposes} CanVisit:{CanVisitAll} CanV:{CanVisitResult[0]},{CanVisitResult[2]}, CannotV:{CannotVisitResult[0]},{CannotVisitResult[2]}")
    if CanVisitAll:
        return CanVisitResult
    return CannotVisitResult

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
   


def RevertKeys(keys):
    res = []
    for k in keys:
        if k == 'B':
            continue
        i = Dirs.index(k)
        res.append(Dirs[(i+2)%4])
    return res
    