from distributed.storage.src.driver.client.default.south import ClientSouthDriver
from distributed.storage.src.driver.client.default.west import ClientWestDriver
from distributed.storage.src.driver.db.endpoint.default import DefaultEndPointDB

from distributed.storage.src.api.client.south import ClientSouthAPI
from distributed.storage.src.api.client.west import ClientWestAPI

from distributed.storage.src.config.config import DSConfig

from distributed.storage.src.util.packetmanager import PacketManager

from distributed.storage.src.channel.engine import ChannelEngine

from distributed.storage.src.driver.controller.default.south import ControllerSouthDriver
from distributed.storage.src.test.mock.db.mockeddb import MockedDB

import unittest
import os
import time
import uuid
import xmlrpclib

class ClientManagerTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_configure(self):
        pass

    def test_start(self):
        pass

    def test_upload_file(self, file, requirements):
        pass

    def test_download_file(self, file_id):
        pass

    def test_configure_south_backend(self, data_ip, data_port):
        pass

    def test_configure_west_backend(self):
        pass

    def test_configure_north_backend(self):
        pass

    def test_send(self, servers, file):
        pass

    def test_receive(self, file_id):
        pass

    def test_construct_file(self, file_chunks):
        pass

    def test_split_file(self, file):
        pass

    def test_mount_channel(self, url, channel_type):
        pass

    def test_alert(self, func, **kwargs):
        pass

    def test_process_ping(self, **kwargs):
        #TODO
        pass

    def test_process_syn_request(self, **kwargs):
        #TODO
        pass

    def test_process_read(self, **kwargs):
        #TODO
        pass

    def test_process_write(self, **kwargs):
        pass


if __name__ == "__main__":
    unittest.main()