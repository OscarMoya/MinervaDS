from distributed.storage.src.api.server.west import ServerWestAPI
from distributed.storage.src.api.server.north import ServerNorthAPI
from distributed.storage.src.api.server.south import ServerSouthAPI

from distributed.storage.src.driver.controller.default.south import ControllerSouthDriver
from distributed.storage.src.driver.server.default.west import ServerWestDriver
from distributed.storage.src.driver.server.default.south import ServerSouthDriver
from distributed.storage.src.driver.db.endpoint.default import DefaultEndPointDB

from distributed.storage.src.config.config import DSConfig
from distributed.storage.src.channel.engine import ChannelEngine

from distributed.storage.src.util.packetmanager import PacketManager

import time
import uuid
import xmlrpclib

class ServerManager:

    def __init__(self, db=None, id=None):
        if not id:
            id = uuid.uuid4()

        self.__nf_manager = None

        self.__type = DSConfig.SERVER_TYPE
        self.__default_mgmt_port = DSConfig.DEFAULT_MGMT_PORT
        self.__default_data_port = DSConfig.DEFAULT_DATA_PORT

        self.__north_backend = None
        self.__east_backend = None
        self.__west_backend = None
        self.__south_backend = None

        self.__id = id
        self.__db = db

        self.configure()

    def configure(self):
        self.__configure_west_backend()
        self.__configure_south_backend()
        self.__configure_north_backend()


    def __configure_west_backend(self):
        pipe = self
        db = DefaultEndPointDB()
        driver = ServerWestDriver(db, pipe)
        api = ServerWestAPI(driver)
        self.__west_backend = api


    def __configure_south_backend(self):
        packet_manager = PacketManager
        pipe = self
        driver = ServerSouthDriver(packet_manager, pipe)
        api = ServerSouthAPI(driver)

        self.__south_backend = api


    def __configure_north_backend(self):
        packet_manager = PacketManager
        pipe = self
        driver = ControllerSouthDriver(packet_manager, pipe)
        api = ServerNorthAPI(driver)
        self.__north_backend = api


    def start(self, mgmt_ip, mgmt_port, data_ip, data_port):
        self.__south_backend.start(mgmt_ip, mgmt_port)
        self.__west_backend.start(data_ip, data_port)
        self.__north_backend.join(self.__id, self.__type, mgmt_ip, data_ip)
        if self.__db:
            self.__db.load_all()



    def alert(self, func, **kwargs):
        if func.__name__ == "ping":
            return self.__process_ping(**kwargs)
        elif func.__name__ == "write_request":
            return self.__process_write_request(**kwargs)
        elif func.__name__ == "read_request":
            return self.__process_read_request(**kwargs)


    def __process_write_request(self, **kwargs):
        #TODO implement this function
        pass


    def __process_read_request(self, **kwargs):
        pass


    def __process_ping(self, **kwargs):
        pass


    def send_to(self, file_id, endpoint_params):
        pass


    def get_north_backend(self):
        return self.__north_backend


    def get_south_backend(self):
        return self.__south_backend


    def get_east_backend(self):
        return self.__east_backend


    def get_west_backend(self):
        return self.__west_backend

    def get_id(self):
        return self.__id

