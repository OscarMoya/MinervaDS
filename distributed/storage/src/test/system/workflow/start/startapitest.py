from SimpleXMLRPCServer import SimpleXMLRPCServer
import unittest
from distributed.storage.src.api.controller.south import ControllerSouthAPI
from distributed.storage.src.driver.controller.default.south import ControllerSouthDriver
from distributed.storage.src.driver.db.endpoint.default import DefaultEndPointDB
from distributed.storage.src.module.client.manager import ClientManager
from distributed.storage.src.module.controller.manager import ControllerManager
from distributed.storage.src.test.mock.client.mockedchannel import MockedChannel
import xmlrpclib
from distributed.storage.src.util.threadmanager import ThreadManager

import sys

class ControllerSouthBackendTest(unittest.TestCase):

    def setUp(self):
        print "Set UP"
        self.manager = ControllerManager()

        self.south_backend = self.manager.get_south_backend()
        try:
            self.south_backend.start("10.10.253.1", 9696)
        except:
            pass
        self.client = xmlrpclib.ServerProxy("http://10.10.253.1:9696")

    def tearDown(self):
        pass

    def test_should_join(self):
        result = self.client.join("ID", "Client", "10.10.253.1", "10.10.254.1")
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
    sys.exit()
