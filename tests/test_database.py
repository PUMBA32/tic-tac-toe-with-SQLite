import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from database import Database


class TestDatabase(unittest.TestCase):
    def test_get_all_player(self): 
        db: Database = Database()
        
        self.assertEqual(type(db.get_all_player()), list)
        
        db.close_db()
    

    def test_assert_update_data_by_name(self): 
        db: Database = Database()
        
        self.assertRaises(ValueError, db.update_data_by_name, 'tyler', 1.0, 1)
        self.assertRaises(ValueError, db.update_data_by_name, 'tyler', 1, 1.0)
        self.assertRaises(ValueError, db.update_data_by_name, 'tyler', True, 10)
        self.assertRaises(ValueError, db.update_data_by_name, 'tyler', True, False)
        self.assertRaises(ValueError, db.update_data_by_name, 'tyler', 1, "10")
        self.assertRaises(ValueError, db.update_data_by_name, 'tyler', None, "")
        self.assertRaises(ValueError, db.update_data_by_name, None, 1, 1)

        db.close_db()


if __name__ == '__main__':
    unittest.main()