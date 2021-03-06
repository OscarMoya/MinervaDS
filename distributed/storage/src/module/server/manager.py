import threading
import xmlrpclib
from distributed.storage.src.channel.engine import ChannelEngine
from distributed.storage.src.config.config import DSConfig

from distributed.storage.src.api.server.west import ServerWestAPI
from distributed.storage.src.api.server.north import ServerNorthAPI
from distributed.storage.src.api.server.south import ServerSouthAPI
from distributed.storage.src.driver.db.file.default import DefaultFileDB

from distributed.storage.src.driver.server.default.west import ServerWestDriver
from distributed.storage.src.driver.server.default.south import ServerSouthDriver
from distributed.storage.src.driver.controller.default.south import ControllerSouthDriver


import uuid
from distributed.storage.src.util.packetmanager import PacketManager
from distributed.storage.src.util.threadmanager import ThreadManager


class ServerManager:

    def __init__(self, db=None, id=None):
        if not id:
            id = uuid.uuid4()

        if not db:
            db = DefaultFileDB("server")

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


    def __configure_west_backend(self):
        pipe = self
        db = DefaultFileDB("server")
        self.__west_db = db
        driver = ServerWestDriver(db=self.__west_db, pipe=pipe)
        api = ServerWestAPI(driver)
        self.__west_backend = api

    def __start_north_backend(self):
        controller_url = DSConfig.CONTROLLER_URL
        controller_iface = xmlrpclib.ServerProxy(controller_url)
        self.__north_backend = controller_iface


    def __configure_south_backend(self):
        pipe = self
        packet_manager = PacketManager
        driver = ServerSouthDriver(packet_manager=packet_manager, pipe=pipe)
        api = ServerSouthAPI(driver)

        self.__south_backend = api

    def start(self, mgmt_ip, mgmt_port, data_ip, data_port):
        self.__south_backend.start(mgmt_ip, mgmt_port)
        self.__west_backend.start(data_ip, data_port)
        self.__start_north_backend()

        data_url = "http://"+ data_ip + ":" + str(data_port)
        mgmt_url = "http://"+ mgmt_ip + ":" + str(mgmt_port)

        result = ThreadManager.start_method_in_new_thread(self.__north_backend.join, [self.__id, self.__type, mgmt_url, data_url])
        if self.__db:
            self.__db.load()
        return result

    def alert(self, func, **kwargs):
        if func == "write":
            self.__process_write(**kwargs)
        elif func == "ping":
            self.__process_ping(**kwargs)
        elif func == "controller_write_request":
            self.__send_to_client(**kwargs)
        else:
            pass
        pass

    def __process_write(self, **kwargs):
        
        pass

    def __process_ping(self, **kwargs):
        
        pass

    def send_to(self, file_id, endpoint_params):
        
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

    def get_db(self):
        return self.__db

    def __send_to_client(self, **kwargs):
        client = self.__mount_channel(kwargs.get("channel"), kwargs.get("client_url"))
        file_entry = self.__west_db.filter(chunk_id=kwargs.get("chunk_id"))[0]
        chunk_type = file_entry.get(kwargs.get("chunk_id")).get("chunk_type")
        data = file_entry.get(kwargs.get("chunk_id")).get("file_data")
        ThreadManager.start_method_in_new_thread(client.write, [data, chunk_type,kwargs.get("chunk_id")])

    def __mount_channel(self, channel_type, url):
        engine = ChannelEngine()
        channel = engine.load_type(channel_type)
        channel = channel(url)
        channel.start()
        return channel

    def disconnect(self):
        self.__north_backend.leave(self.__id)
        return True


