from distributed.storage.src.driver.db.default.default import DefaultDB
import os
try:
    import cPickle as pickle
except:
    import pickle

import unittest
import threading

class DBTest(unittest.TestCase):

    def setUp(self):
        self.db = DefaultDB()
        self.db_name = "test"
        self.db.DB_NAME = self.db_name
        self.default_entry = {"id":777, "a":"data", "b":"more_data"}
        self.default_entry_keys = self.default_entry.keys()
        self.default_entry_values = self.default_entry.values()
        self.default_entry_keys.remove("id")
        self.default_entry_keys.sort()
        self.default_entry_values.remove(777)
        self.default_entry_values.sort()

    def tearDown(self):
        with threading.Lock():
            f = open(self.db_name, "w+")
            f.write("")
            f.close()

    def test_should_save_data(self):
        self.db.save(**self.default_entry)
        f = open("test","r")
        stored_data = pickle.load(f)

        f.close()

        keys = stored_data.get(777).keys()
        keys.sort()
        values = stored_data.get(777).values()
        values.sort()
        self.assertEquals(self.default_entry_keys, keys)
        self.assertEquals(self.default_entry_values, values)

    def test_should_load_data(self):
        self.db.save(**self.default_entry)
        data = self.db.load(id=777)

        keys = data[0].get(777).keys()
        keys.sort()
        values = data[0].get(777).values()
        values.sort()

        self.assertEquals(self.default_entry_keys, keys)
        self.assertEquals(self.default_entry_values, values)

    def test_should_remove_data(self):
        self.db.save(**self.default_entry)

        self.db.remove(id=777)
        f = open("test","r")
        stored_data = pickle.load(f)

        f.close()
        self.assertTrue(stored_data == {})


if __name__ == "__main__":
    unittest.main()