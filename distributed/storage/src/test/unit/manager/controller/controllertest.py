from distributed.storage.src.module.controller.manager import ControllerManager
from distributed.storage.src.driver.client.default.south import ClientSouthDriver
from distributed.storage.src.driver.db.endpoint.default import DefaultEndPointDB
from distributed.storage.src.driver.db.file.default import DefaultFileDB

import unittest

class ControllerManagerTest(unittest.TestCase):

    def setUp(self):
        self.id = "FancyController"
        self.manager = ControllerManager()

        self.client = ClientSouthDriver()
        self.db_endpoint = DefaultEndPointDB()
        self.filedb = DefaultFileDB

    def test_should_start(self):
        #TODO: Fails
        self.manager.start()

    def test_should_alert(self):
        pass

    def test_should_process_join_event(self):
        pass

    def test_should_process_leave_event(self):
        pass

    def test_should_process_read_request_event(self):

        pass

    def test_should_process_write_request_event(self):

        pass

    def test_should_add_endpoint(self):
        pass

    def test_should_remove_endpoint(self):
        pass

    def test_should_mount_endpoint(self):
        pass

if __name__ == "__main__":
    unittest.main()
