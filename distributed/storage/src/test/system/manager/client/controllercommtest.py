from distributed.storage.src.module.client.manager import ClientManager
from distributed.storage.src.module.controller.manager import ControllerManager
from distributed.storage.src.driver.db.endpoint.default import DefaultEndPointDB
from distributed.storage.src.driver.db.file.default import DefaultFileDB
from distributed.storage.src.config.config import DSConfig
import xmlrpclib
import subprocess
import unittest
import os
import signal

class ControllerCommunicationTest(unittest.TestCase):

    def setUp(self):
        self.mgmt_ip = "10.10.253.1"
        self.data_ip = "10.10.253.2"
        self.mgmt_port = 9696
        self.data_port = 9595

        self.db_endpoint = DefaultEndPointDB()
        self.file_db = DefaultFileDB()

        self.manager = ClientManager(db=self.file_db, id="fancyClient")
        self.ctrl_manager = ControllerManager()

        self.ctrl_manager.start(self.mgmt_ip, self.mgmt_port)

        s = xmlrpclib.ServerProxy("http://10.10.254.1:9696/RPC2")
        print s.ping()
        self.manager.start(self.mgmt_ip, self.mgmt_port, self.data_ip, self.data_port)

        self.requirements = None
        self.file_id = "F4NC1_F1L3"
        self.file = ""

    def test_should_check_controller_API(self):
        print "fa", self.manager.get_north_backend()

    def test_should_upload_file(self):
        pass

    def test_should_download_file(self):
        pass

if __name__ == "__main__":
    unittest.main()
