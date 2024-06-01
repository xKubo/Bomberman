
import unittest
import utils

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



if __name__ == '__main__':
    unittest.main()