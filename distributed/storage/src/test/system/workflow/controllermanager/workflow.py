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
import time
import sys

class ControllerSouthBackendWorkFlow(unittest.TestCase):

    def setUp(self):
        self.manager = ControllerManager()
        self.manager.start("10.10.253.1", 9696)
        self.client = xmlrpclib.ServerProxy("http://10.10.253.1:9696")

    def test_workflow(self):
        print "Client Manager started, preparing join"
        result = self.client.join("ID", "Client", "10.10.253.1", "10.10.254.1")
        self.check_join_result(result)
        self.check_saved_endpoints()
        print "Client Manager Join Process. OK"
        time.sleep(1)

        print "Client Manager, Preparing Leave"
        result = self.client.leave("ID")
        self.check_leave_result(result)
        self.check_endpoints_are_null()
        print "Results Checked"

    def tearDown(self):
        pass

    def check_join_result(self, result):
        self.assertTrue(result)

    def check_saved_endpoints(self):
        expected_params = ["Client", "http://10.10.253.1:9696", "10.10.254.1"]
        expected_params.sort()
        actual_params = self.manager.active_endpoints.get("ID").values()
        actual_params.sort()
        self.assertEquals(expected_params, actual_params)

    def check_endpoints_are_null(self):
        self.assertEquals(0, len(self.manager.active_endpoints.keys()))

    def check_leave_result(self, result):
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()
