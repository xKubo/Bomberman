
import unittest
import utils
import Vec2d

import testMap


class TestException(unittest.TestCase):
    def Throw(self):
        raise utils.Error("test")
    
    def test_Exception(self):
        self.assertRaises(utils.Error, self.Throw)

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())


class TestVector(unittest.TestCase):
    def test_Equality(self):
        self.assertTrue(Vec2d.Vector2D(10, 3), Vec2d.Vector2D(10, 3))

if __name__ == '__main__':
    unittest.main()