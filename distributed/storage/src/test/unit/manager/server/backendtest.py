from distributed.storage.src.module.server.manager import ServerManager
from distributed.storage.src.driver.db.endpoint.default import DefaultEndPointDB
import unittest

class ServerGenericBackendTest(unittest.TestCase):

    def setUp(self):
        self.id = "FancyID"
        self.manager = ServerManager(id=self.id,  db=DefaultEndPointDB())

    def test_should_have_id(self):
        self.assertEquals(self.id, self.manager.get_id())

    def test_should_have_north_backend(self):
        self.assertFalse(self.manager.get_north_backend()==None)

    def test_should_have_south_backend(self):
        self.assertFalse(self.manager.get_south_backend()==None)

    def test_should_not_have_east_backend(self):
        '''
        East backends are dynamically configured
        '''
        self.assertTrue(self.manager.get_east_backend()==None)

    def test_should_have_west_backend(self):
        self.assertFalse(self.manager.get_west_backend()==None)


if __name__ == "__main__":
    unittest.main()
