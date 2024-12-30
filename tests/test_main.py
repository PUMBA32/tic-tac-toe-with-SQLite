import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'main')))

from main import Menu


class TestMenu(unittest.TestCase): 
    def test_raises_show_menu(self):
        menu = Menu()
        
        self.assertRaises(ValueError, menu.show_menu, 1.0)
        self.assertRaises(ValueError, menu.show_menu, "nigger")
        self.assertRaises(ValueError, menu.show_menu, True)
        self.assertRaises(ValueError, menu.show_menu, 1+3j)


if __name__ == '__main__':
    unittest.main()