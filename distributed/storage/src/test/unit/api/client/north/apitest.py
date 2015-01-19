from distributed.storage.src.api.client.north import ClientNorthAPI
from distributed.storage.src.test.mock.client.mockedchannel import MockedChannel
import unittest

class NorthApiTest(unittest.TestCase):

    def setUp(self):
        self.api = ClientNorthAPI()
        self.mocked_channel = MockedChannel()

        self.api.set_controller_north_channel(self.mocked_channel)

    def test_should_join(self):
        self.assertTrue(self.api.join( None, None, None))

    def test_should_leave(self):
        self.assertTrue(self.api.leave(None))

    def test_should_read_request(self):
        self.assertTrue(self.api.read_request(None, None))

    def test_should_write_request(self):
        self.assertTrue(self.api.write_request(None,None))

if __name__ == "__main__":
    unittest.main()
