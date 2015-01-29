from distributed.storage.src.module.server.manager import ServerManager
from distributed.storage.src.config.config import DSConfig

import subprocess

import unittest
import os
import signal

class ControllerCommunicationTest(unittest.TestCase):

    def setUp(self):
        self.mgmt_ip = "10.10.254.1"
        self.data_ip = "10.10.253.1"
        self.mgmt_port = 9696
        self.data_port = 9595

        self.manager = ServerManager(id="FancyId")
        self.manager.start(self.mgmt_ip, self.mgmt_port, self.data_ip, self.data_port)




    def test_should_check_controller_API(self):

        print "-------------O", self.manager.get_north_backend()


if __name__ == "__main__":
    unittest.main()

