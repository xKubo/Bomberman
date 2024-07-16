from Vec2d import Vector2D
import utils
import unittest


class TestNeighboringFields(unittest.TestCase):
    def NFields(self, pos, tolerance = 20):
        fields = utils.NeighboringFields(Vector2D(*pos), tolerance)
        return list(map(lambda f: f.to_tuple(), fields))

    def CheckFields(self, result, expected):
        s1 = set(result)
        s2 = set(expected)
        self.assertEqual(s1, s2)

    def test_OneExactPosition(self):
        fields = self.NFields((0,0))
        self.CheckFields(fields, [(0,0)])
        
    def test_TwoFields(self):
        fields = self.NFields((25,0))
        self.CheckFields(fields, [(0,0), (0,1)])
        
    def test_FourFields(self):
        fields = self.NFields((25,25))
        self.CheckFields(fields, [(0,0), (1,0), (0,1), (1,1)])
        
    def test_FourFieldsLeftUpperQuadrant(self):
        fields = self.NFields((475,475))  # best field is [5,5]
        self.CheckFields(fields, [(5,5), (4,5), (5,4), (4,4)])
        
    def test_FourFieldsLeftUpperQuadrantInTolerance(self):
        fields = self.NFields((485,485))  # best field is [5,5]
        self.CheckFields(fields, [(5,5)])


class TestFieldsInDirection(unittest.TestCase):
    def TestFields(self, posMiddle, dir, output, tolerance = 20):
        fieldsvec = utils.FieldsInDirection(Vector2D(*posMiddle), utils.DirToVec[dir], tolerance)
        fieldstup = set(map(lambda fv: fv.to_tuple(), fieldsvec))
        self.assertEqual(fieldstup, set(output))        
    
    def test_UpOne(self):
        self.TestFields((150, 150), 'U', [(1,0)])

    def test_UpTwoLeft(self):
        self.TestFields((100, 150), 'U', [(0,0), (1,0)])

    def test_DownOne(self):
        self.TestFields((150, 150), 'D', [(1,2)])

    def test_DownTwoLeft(self):
        self.TestFields((100, 150), 'D', [(0,2), (1,2)])
        
    def test_LeftOne(self):
        self.TestFields((150, 150), 'L', [(0,1)])

    def test_LeftTwoUp(self):
        self.TestFields((150, 100), 'L', [(0,1), (0,0)])

        
        
if __name__ == '__main__': 
    unittest.main()
    