from distributed.storage.src.driver.controller.default.south import ControllerSouthDriver
from distributed.storage.src.test.mock.db.mockeddb import MockedDB
import unittest

class ControllerSouthDriverTest(unittest.TestCase):

    def setUp(self):
        self.driver = ControllerSouthDriver()
        self.db = MockedDB()
        self.driver.set_file_db(MockedDB())
        self.driver.set_endpoint_db(MockedDB())
        self.expected_keys = ["A", "AxB", "B"]
        self.expected_values = ["URL_A", "URL_AxB", "URL_B"]
        self.expected_keys.sort()
        self.expected_values.sort()

    def test_should_join(self):
        result = self.driver.join("paramA", "paramB", "paramC", "paramD")
        self.assertTrue(result)
        self.assertEquals(self.db.random_entry.keys()[0] ,self.driver.get_endpoint_db().value.keys()[0])

    def test_should_leave(self):
        result = self.driver.leave("paramA")
        self.assertTrue(result)
        self.assertEquals(0 , len(self.driver.get_endpoint_db().value.keys()))

    def test_should_read_request(self):
        result = self.driver.read_request(None, None)
        obtained_keys = result.keys()
        obtained_values = result.values()
        obtained_keys.sort()
        obtained_values.sort()
        self.assertEquals(self.expected_keys, obtained_keys)
        self.assertEquals(self.expected_values, obtained_values)

    def test_should_write_request(self):
        result = self.driver.write_request("None", "None", None)
        self.assertFalse(result.pop("file_id")==None)
        obtained_keys = result.keys()
        obtained_values = result.values()
        obtained_keys.sort()
        obtained_values.sort()
        self.assertEquals(self.expected_keys, obtained_keys)
        self.assertEquals(self.expected_values, obtained_values)


if __name__ == "__main__":
    unittest.main()
