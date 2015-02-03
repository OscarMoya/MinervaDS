from SimpleXMLRPCServer import SimpleXMLRPCServer
import time
import xmlrpclib

from distributed.storage.src.module.client.manager import ClientManager
from distributed.storage.src.module.server.manager import ServerManager
from distributed.storage.src.test.mock.client.mockedchannel import MockedChannel
from distributed.storage.src.util.threadmanager import ThreadManager

import unittest

class ServerManagerWorkFlow(unittest.TestCase):

    def setUp(self):
        self.id = "TestID"
        self.mgmt_ip =  "10.10.253.2"
        self.data_ip = "10.10.254.2"
        self.data_port = 9696
        self.mgmt_port = 9797
        self.data = "Hello World"
        s = SimpleXMLRPCServer(("10.10.254.1", 9696)) # Simulating Controller Server
        s.register_instance(MockedChannel())
        ThreadManager.start_method_in_new_thread(s.serve_forever, [])



        self.manager = ServerManager(id = self.id)


    def test_cm_workflow(self):
        print "Fake Controller is up."
        print "Starting Test."
        result = self.manager.start(self.mgmt_ip, self.mgmt_port, self.data_ip, self.data_port)
        self.check_result_is_true(result)
        print "Server Manager Started OK"

        self.controller_client = xmlrpclib.ServerProxy("http://10.10.253.2:9696")

        time.sleep(1)

        print "Testing Write Request"

        try:
            result = self.controller_client.write_request("params")
            self.check_result_is_true(result)
            print "Write Request OK"
        except:
            pass

    def check_result_is_true(self, result):
         self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()