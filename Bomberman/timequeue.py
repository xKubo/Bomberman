import bisect

class TimeQueue:
    
    comp = lambda to: to[0]

    def __init__(self) -> None:
        self.timequeue = []
        
    def AddTimeObject(self, at, fn):
        bisect.insort_right(self.timequeue, (at, fn),  key=TimeQueue.comp)
        
    def GetOlderOrEqual(self, at):
        i = bisect.bisect_right(self.timequeue, at, key=TimeQueue.comp)
        older = self.timequeue[:i]
        self.timequeue = self.timequeue[i:]      
        return older

    def RemoveTimeObject(self, at, num):
        pass