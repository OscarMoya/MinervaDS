from distributed.storage.src.driver.client.default.south import ClientSouthDriver
from distributed.storage.src.test.mock.util.mockedpacketmanager import MockedPacketManager

import unittest

class ClientDriverTest(unittest.TestCase):

    def setUp(self):
        self.driver = ClientSouthDriver()
        self.packet_manager = MockedPacketManager()
        self.driver.set_packet_manager(self.packet_manager)

    def test_should_ping(self):
        self.assertEquals("PONG", self.driver.ping())

    def test_should_send_packet_syn(self):
        self.assertEquals(True, self.driver.syn_request())

if __name__=="__main__":
    unittest.main()

