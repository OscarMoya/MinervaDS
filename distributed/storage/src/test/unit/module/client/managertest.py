from distributed.storage.src.module.client.manager import ClientManager
from distributed.storage.src.module.nf.manager import NF_Manager
from distributed.storage.src.test.mock.db.mockeddb import MockedDB

import unittest
import os
import time
import uuid
import xmlrpclib

class ClientManagerTest(unittest.TestCase):
    def setUp(self):
        self.manager = ClientManager(db=MockedDB(), id="Client")
        self.manager.__nf_manager = NF_Manager()

        self.file_chunks = [{"type": "A", "value": "AAAAAA"},
                           {"type": "B", "value": "BBBBBB"},
                           {"type": "AxB", "value": "CCCCCC"}]

        self.expected_keys = ["A", "B", "AxB"]
        self.expected_values = ["AAAAAA", "BBBBBB", "CCCCCC"]
        self.expected_file = "AAAAAABBBBBBCCCCCC"

        self.expected_result = None
        self.expected_keys.sort()
        self.expected_values.sort()

    def test_configure(self):
        result = self.manager.configure()
        self.assertTrue(result)

    def test_start(self):
        result = self.manager.start("paramA", "paramB", "paramC", "paramD")
        self.assertTrue(result)

    def test_upload_file(self):
        result = self.manager.upload_file(self.expected_file)
        pass

    def test_download_file(self):
        pass

    def test_configure_south_backend(self):
        pass

    def test_configure_west_backend(self):
        pass

    def test_configure_north_backend(self):
        pass

    def test_send(self):
        pass

    def test_receive(self):
        pass

    def test_construct_file(self):
        result = self.manager.__construct_file(self.file_chunks)
        self.assertTrue(result)
        self.assertEquals(result, self.expected_file)

    def test_split_file(self):
        result = self.manager.__split_file(self.expected_file)
        self.assertTrue(result)
        self.assertEquals(result, self.file_chunks)

    def test_mount_channel(self):
        pass

    def test_alert(self):
        pass

    def test_process_ping(self):
        #TODO
        pass

    def test_process_syn_request(self):
        #TODO
        pass

    def test_process_read(self):
        #TODO
        pass

    def test_process_write(self):
        pass

    def test_get_file_size(self):
        result = self.manager.__get_file_size(self.expected_file)
        return result
        #self.assertTrue(result)
        #self.assertEquals(result, self.expected_result)

if __name__ == "__main__":
    #unittest.main()
    test = ClientManagerTest()
    result = test.test_get_file_size()
    print result