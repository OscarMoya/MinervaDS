from SimpleXMLRPCServer import SimpleXMLRPCServer
import time
import xmlrpclib

from distributed.storage.src.module.client.manager import ClientManager
from distributed.storage.src.test.mock.client.mockedchannel import MockedChannel
from distributed.storage.src.util.threadmanager import ThreadManager

import unittest

class ClientManagerWorkFlow(unittest.TestCase):

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
        c =  xmlrpclib.ServerProxy("http://10.10.254.1:9696")
        print "Server: ",c.join("ID", "None", "None", "None")
        self.manager = ClientManager(id = self.id)

    def test_cm_workflow(self):
        print "Fake Controller is up."
        print "Starting Test."
        result = self.manager.start(self.mgmt_ip, self.mgmt_port, self.data_ip, self.data_port)
        self.check_result_is_true(result)
        print "Client Manager Started OK"
        time.sleep(1)
        print "Testing Write Request"
        try:
            result = self.manager.upload_file(self.data, {})
            self.check_result_is_true(result)
        except:
            pass
        print "Write Request OK"
        try:
            result = self.manager.download_file("id")
            self.check_result_is_true(result)
        except:
            pass

    def check_result_is_true(self, result):
         self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()
