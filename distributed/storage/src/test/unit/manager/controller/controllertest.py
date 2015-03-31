from distributed.storage.src.module.controller.manager import ControllerManager
from distributed.storage.src.driver.client.default.south import ClientSouthDriver
from distributed.storage.src.driver.controller.default.south import ControllerSouthDriver
from distributed.storage.src.driver.db.endpoint.default import DefaultEndPointDB
from distributed.storage.src.driver.db.file.default import DefaultFileDB

from distributed.storage.src.test.mock.db.mockeddb import MockedDB

import unittest

class ControllerManagerTest(unittest.TestCase):

    def setUp(self):
        self.id = "FancyController"
        self.manager = ControllerManager()

        self.client = ClientSouthDriver()
        self.db_endpoint = DefaultEndPointDB()
        self.filedb = DefaultFileDB
        self.controller = ControllerSouthDriver(None, self.db_endpoint, None)

    def test_should_start(self):
        self.manager.start("10.100.10.50", 9090)

    def test_should_alert(self):
        params = {"id": "A", "type": "client", "mgmt_ip": "10.100.10.71", "data_ip": "192.168.1.10"}
        self.assertTrue(self.manager.alert(self.controller.read_request)==None)
        self.assertTrue(self.manager.alert(self.controller.write_request)==None)

if __name__ == "__main__":
    unittest.main()
