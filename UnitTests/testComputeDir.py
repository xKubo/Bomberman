from arena import ComputeNewDir, EmptyDir
import unittest

def CanGo(CanGoValues):
    def _CanGo(v):
        return v in CanGoValues
    return _CanGo

class TestComputeNewDir(unittest.TestCase):
    def test_StopMoving(self):
        self.assertEqual(ComputeNewDir('L', EmptyDir, True), EmptyDir)
    def test_SameDir(self):
        self.assertEqual(ComputeNewDir('L', 'L', True), 'L')
    def test_OppositeDir(self):
        self.assertEqual(ComputeNewDir('L', 'R', True), 'R')
    def test_CantGoUpHaveToGoLeft(self):
        self.assertEqual(ComputeNewDir('L', 'LU', CanGo('D')), 'L')
    def test_GoUpCameFromRight(self):
        self.assertEqual(ComputeNewDir('L', 'LU', CanGo('UL')), 'U')
    def test_GoLeftCameFromDown(self):
        self.assertEqual(ComputeNewDir('U', 'LU', CanGo('UL')), 'L')
    def test_CantButTryToGoLeft(self):
        self.assertEqual(ComputeNewDir('L', 'LU', CanGo('')), 'L')                 
    def test_GoRightCameFromUp(self):
        self.assertEqual(ComputeNewDir('D', 'DR', CanGo('DR')), 'R') 
    def test_GoDownCameFromRight(self):
        self.assertEqual(ComputeNewDir('R', 'DR', CanGo('DR')), 'D') 
        