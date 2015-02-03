import unittest

from distributed.storage.src.module.client.manager import ClientManager
from distributed.storage.src.module.controller.manager import ControllerManager
from distributed.storage.src.module.server.manager import ServerManager

from distributed.storage.src.config.config import DSConfig

class startTest(unittest.TestCase):

    def setUp(self):
        pass

    def configure_client(self):
        pass

    def configure_server(self):
        pass

    def configure_controller(self):
        id = "FancyController"
        self.controller_manager = ControllerManager()
        self.controller_manager.start("10.10.254.1", DSConfig.DEFAULT_MGMT_PORT)

