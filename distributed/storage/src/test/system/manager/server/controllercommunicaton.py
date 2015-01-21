from distributed.storage.src.module.server.manager import ServerManager
from distributed.storage.src.config.config import DSConfig

import subprocess

import unittest

class ControllerCommunicationTest(unittest.TestCase):

    def setUp(self):

        self.configure_interfaces()

        self.mgmt_ip = "10.10.254.2"
        self.data_ip = "10.10.253.2"
        self.mgmt_port = 9696
        self.data_port = 9595

        self.manager = ServerManager(id="FancyId")
        self.manager.start(self.mgmt_ip, self.mgmt_port, self.data_ip, self.data_port)


    def test_should_check_controller_API(self):

        print "-------------O", self.manager.get_north_backend()

    def configure_interfaces(self):
        #add_interface = "vconfig add eth0 1000"
        #up_interface = "ifconfig eth0.1000 up"
        #set_ip = "ifconfig eth0.1000 %s" % DSConfig.CONTROLLER_URL
        #subprocess.call(add_interface, stdout=subprocess.PIPE)
        #subprocess.call(up_interface, stdout=subprocess.PIPE)
        #subprocess.call(set_ip, stdout=subprocess.PIPE)
        pass


if __name__ == "__main__":
    unittest.main()