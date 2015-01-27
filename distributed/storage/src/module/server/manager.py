from distributed.storage.src.config.config import DSConfig

from distributed.storage.src.api.server.west import ServerWestAPI
from distributed.storage.src.api.server.north import ServerNorthAPI
from distributed.storage.src.api.server.south import ServerSouthAPI

from distributed.storage.src.driver.server.default.west import ServerWestDriver
from distributed.storage.src.driver.server.default.south import ServerSouthDriver
from distributed.storage.src.driver.controller.default.south import ControllerSouthDriver

from distributed.storage.src.driver.db.endpoint.default import DefaultEndPointDB

import uuid


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

    def __configure_north_backend(self):
        api = ServerNorthAPI()
        self.__north_backend = api

    def __configure_south_backend(self):
        pipe = self
        db = DefaultEndPointDB()
        driver = ServerSouthDriver(db, pipe)
        api = ServerSouthAPI(driver)

        self.__south_backend = api

    def start(self, mgmt_ip, mgmt_port, data_ip, data_port):
        #TODO: Doesn't work, start() takes exactly 2 arguments (3 given)
        self.__south_backend.start(mgmt_ip, mgmt_port)
        self.__west_backend.start(data_ip, data_port)
        self.__north_backend.start(DSConfig.CONTROLLER_URL)
        self.__north_backend.join(self.__id, self.__type, mgmt_ip, data_ip)
        if self.__db:
            self.__db.load_all()

    def alert(self, func, **kwargs):
        #TODO: Implement
        if func.__name__ == "write":
            self.__process_write(**kwargs)
        elif func.__name__ == "ping":
            self.__process_ping(**kwargs)
        else:
            #TODO See what we can do
            pass
        pass

    def __process_write(self, **kwargs):
        #TODO: Implement, Log The Call
        pass

    def __process_ping(self, **kwargs):
        #TODO: Implement, Log The Call
        pass

    def send_to(self, file_id, endpoint_params):
        #TODO: Implement
        pass

    def get_id(self):
        return self.__id

    def get_north_backend(self):
        return self.__north_backend

    def get_south_backend(self):
        return self.__south_backend

    def get_west_backend(self):
        return self.__west_backend

    def get_east_backend(self):
        return self.__east_backend
