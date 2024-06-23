from sprites import TimeLine
import unittest

class TestTimeline(unittest.TestCase):
    def Check(self, TickMS, FrameTimeMS, Frames, Output):
        cfg = {"frame_time":FrameTimeMS, "tick_ms":TickMS}
        if isinstance(Frames, int):
           cfg["frames"] = [] 
           tl = TimeLine(cfg, Frames)
        elif isinstance(Frames, str):
            cfg["frames"] = [int(f) for f in Frames]
            tl = TimeLine(cfg, 0)
        res = ""
        Counter = 0
        while Counter < tl.TotalTime():
            Counter += TickMS
            tl.Update()
            res += chr(tl.CurrentFrame() + ord('0'))
        self.assertEqual(res, Output)
        
    def test_normal(self):
        self.Check(50, 100, 3, '001122')

    def test_custom(self):
        self.Check(50, 100, '0121', '00112211')

    def test_simple(self):
        self.Check(50, 50, 4, '0123')

if __name__ == '__main__': 
    unittest.main()             