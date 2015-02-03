from SimpleXMLRPCServer import SimpleXMLRPCServer
import unittest
from distributed.storage.src.api.controller.south import ControllerSouthAPI
from distributed.storage.src.driver.controller.default.south import ControllerSouthDriver
from distributed.storage.src.driver.db.endpoint.default import DefaultEndPointDB
from distributed.storage.src.test.mock.client.mockedchannel import MockedChannel
import xmlrpclib
from distributed.storage.src.util.threadmanager import ThreadManager


class ServiceTest(unittest.TestCase):

    def setUp(self):
        self.channel = MockedChannel()

        self.server = SimpleXMLRPCServer(("localhost", 1111))
        self.server.register_instance(self.channel)

        ThreadManager.start_method_in_new_thread(self.server.serve_forever, [])


        self.client = xmlrpclib.ServerProxy("http://localhost:1111")

    def test_should_join(self):
        self.assertTrue(self.client.join())

if __name__ == "__main__":
    unittest.main()






