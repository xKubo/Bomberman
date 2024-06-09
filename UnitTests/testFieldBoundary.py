from utils import FieldBoundary, Vector2D
import unittest

class TestFieldBoundary(unittest.TestCase):
    def Check(self, OldPos, NewPos, exp):
        res = FieldBoundary(Vector2D(*OldPos), Vector2D(*NewPos)).to_tuple()
        self.assertEqual(res, exp)
        
    def test_LeftRight(self):
        self.Check((20, 180), (20, 250), (20, 199))    
        
    def test_RightLeft(self):
        self.Check((20, 150), (20, 80), (20, 100)) 
        
    def test_DownUp(self):
        self.Check((120,200), (3,200), (100,200))
        