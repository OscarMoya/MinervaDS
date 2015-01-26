from distributed.storage.src.module.controller.manager import ControllerManager
from distributed.storage.src.driver.client.default.south import ClientSouthDriver
from distributed.storage.src.driver.controller.default.south import ControllerSouthDriver
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
        self.controller = ControllerSouthDriver()

    def test_should_start(self):
        #TODO: Works!
        self.manager.start("10.100.10.50", 9090)

    def test_should_alert(self):
        #TODO: 'processoutput' object has no attribute '__name__'
        self.assertTrue(self.manager.alert(self.controller.join)==None)
        self.assertTrue(self.manager.alert(self.controller.leave)==None)
        self.assertTrue(self.manager.alert(self.controller.read_request)==None)
        self.assertTrue(self.manager.alert(self.controller.write_request)==None)

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
