from Vec2d import Vector2D
import gamemap
import unittest


class TestNeighboringFields(unittest.TestCase):
    def NFields(self, pos, tolerance = 20):
        fields = gamemap.NeighboringFields(Vector2D(*pos), tolerance)
        return list(map(lambda f: f.to_tuple(), fields))

    def test_OneExactPosition(self):
        fields = self.NFields((0,0))
        self.assertEqual(fields, [(0,0)])
        
    def test_TwoFields(self):
        fields = self.NFields((25,0))
        self.assertEqual(fields, [(0,0), (0,1)])
        
    def test_FourFields(self):
        fields = self.NFields((25,25))
        self.assertEqual(fields, [(0,0), (1,0), (0,1), (1,1)])
        
    def test_FourFieldsLeftUpperQuadrant(self):
        fields = self.NFields((475,475))  # best field is [5,5]
        self.assertEqual(fields, [(5,5), (4,5), (5,4), (4,4)])
        
    def test_FourFieldsLeftUpperQuadrantInTolerance(self):
        fields = self.NFields((485,485))  # best field is [5,5]
        self.assertEqual(fields, [(5,5)])
        
if __name__ == '__main__': 
    unittest.main()
    