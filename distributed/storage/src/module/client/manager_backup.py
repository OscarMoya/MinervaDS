from distributed.storage.src.driver.client.default.south import ClientSouthDriver
from distributed.storage.src.driver.client.default.west import ClientWestDriver
from distributed.storage.src.driver.db.endpoint.default import DefaultEndPointDB
from distributed.storage.src.driver.db.file.default import DefaultFileDB

from distributed.storage.src.api.client.north import ClientNorthAPI
from distributed.storage.src.api.client.south import ClientSouthAPI
from distributed.storage.src.api.client.west import ClientWestAPI

from distributed.storage.src.config.config import DSConfig

from distributed.storage.src.util.packetmanager import PacketManager

from distributed.storage.src.channel.engine import ChannelEngine

from distributed.storage.src.module.nf.manager import NFManager

import os
import time
import uuid
import xmlrpclib
from distributed.storage.src.util.threadmanager import ThreadManager


class ClientManager:

    def __init__(self, db=None, id=None):
        if not id:
            id = uuid.uuid4()
        if not db:
            db = DefaultEndPointDB()

        self.__nf_manager = NFManager()

        self.CHUNK_A_TYPE = "A"
        self.CHUNK_B_TYPE = "B"
        self.CHUNK_AXB_TYPE = "AxB"

        self.__type = DSConfig.CLIENT_TYPE
        self.__default_mgmt_port = DSConfig.DEFAULT_MGMT_PORT
        self.__default_data_port = DSConfig.DEFAULT_DATA_PORT

        self.__north_backend = None
        self.__east_backend = None
        self.__west_backend = None
        self.__south_backend = None

        self.__id = id
        self.__db = db

        self.__requests = dict()
        self.__ready = dict()

        self.configure()

    def configure(self):
        self.__configure_west_backend()
        self.__configure_south_backend()


    def start(self, mgmt_ip, mgmt_port, data_ip, data_port):

        self.__south_backend.start(mgmt_ip, mgmt_port)
        self.__west_backend.start(data_ip, data_port)
        self.__start_north_backend()
        self.__db.load()

        data_url = "http://"+ data_ip + ":" + str(data_port)
        mgmt_url = "http://"+ mgmt_ip + ":" + str(mgmt_port)

        result = ThreadManager.start_method_in_new_thread(self.__north_backend.join, [self.__id, self.__type, mgmt_url, data_url])

    def upload_file(self, file, requirements):
        file_size = "Default"
        servers = self.__north_backend.write_request(self.__id, file_size, requirements)
        result = self.__send(servers, file)
        return result

    def download_file(self, file_id):
        #TODO lock this thread or send the locker
        chunks = self.__north_backend.read_request(self.__id, file_id)
        local_request = dict()
        local_request[file_id] = dict()
        for chunk_id in chunks:
            local_request.get(file_id)[chunk_id] = False

        self.__requests.update(local_request)
        self.__ready[file_id] = False
        while not self.__ready[file_id]:
            True

        chunks = self.__file_db.filter(file_id=file_id)
        file = self.__construct_file(chunks)
        return file

    def __configure_south_backend(self):
        packet_manager = PacketManager
        pipe = self
        driver = ClientSouthDriver(packet_manager, pipe)
        api = ClientSouthAPI(driver)

        self.__south_backend = api

    def __configure_west_backend(self):
        pipe = self
        #endpoint_db = DefaultEndPointDB()
        file_db = DefaultFileDB("client")
        self.__file_db = file_db
        driver = ClientWestDriver(db=file_db, pipe=pipe)
        api = ClientWestAPI(driver)
        self.__west_backend = api

    def __start_north_backend(self):
        controller_url = DSConfig.CONTROLLER_URL
        controller_iface = xmlrpclib.ServerProxy(controller_url)
        self.__north_backend = controller_iface

    def __load_chunks(self, file_id):
        self.__ready[file_id] = True

    def __send(self, servers, file):
        #TODO This should be more or less processed

        server_a = servers.get(self.CHUNK_A_TYPE)
        server_b = servers.get(self.CHUNK_B_TYPE)
        server_axb = servers.get(self.CHUNK_AXB_TYPE)

        channel_a = self.__mount_channel(server_a, servers.get("channel"))
        channel_b = self.__mount_channel(server_b, servers.get("channel"))
        channel_c = self.__mount_channel(server_axb, servers.get("channel"))

        chunk_list = self.__split_file(file)

        chunk_a = chunk_list.pop(0)
        chunk_b = chunk_list.pop(0)
        chunk_c = chunk_list.pop(0)
        del chunk_list

        ThreadManager.start_method_in_new_thread(channel_a.write, [chunk_a.get("value"), servers.get("file_id"),chunk_a.get("type")])
        ThreadManager.start_method_in_new_thread(channel_b.write, [chunk_b.get("value"), servers.get("file_id"),chunk_b.get("type")])
        ThreadManager.start_method_in_new_thread(channel_c.write, [chunk_c.get("value"), servers.get("file_id"),chunk_c.get("type")])

        #result_a = channel_a.write(chunk_a.get("value"), servers.get("file_id"),chunk_a.get("type"))
        #result_b = channel_b.write(chunk_b.get("value"), servers.get("file_id"),chunk_b.get("type"))
        #result_c = channel_c.write(chunk_c.get("value"), servers.get("file_id"),chunk_c.get("type"))

        return True, servers.get("file_id")

    def __receive(self, file_id):
        chunks = self.__requests.get(file_id)
        should_continue = True
        for chunk_key in chunks:
            should_continue = should_continue and chunks[chunk_key]
        if should_continue:
            chunks = self.__load_chunks(file_id)  #TODO Implement
            #return self.__construct_file(chunks)

    def __construct_file(self, file_chunks):
        full_file = self.__nf_manager.reconstruct(file_chunks)
        return full_file

    def __split_file(self, file):
        chunked = self.__nf_manager.deconstruct(file)
        return chunked

    def __mount_channel(self, url, channel_type):
        engine = ChannelEngine()
        channel = engine.load_type(channel_type)
        channel = channel(url)
        channel.start()
        return channel

    def alert(self, func, **kwargs):
        if func == "ping":
            return self.__process_ping(**kwargs)
        elif func == "syn_request":
            return self.__process_syn_request(**kwargs)
        elif func== "read":
            return self.__process_read(**kwargs)
        elif func == "write":
            return self.__process_write(**kwargs)
        else:
            #TODO Raise exception?
            pass

    def __process_ping(self, **kwargs):
        #TODO Log the call
        pass

    def __process_syn_request(self, **kwargs):
        #TODO Log The Call
        pass

    def __process_read(self, **kwargs):
        #TODO
        pass

    def __process_write(self, **kwargs):
        chunk_id = kwargs.get("chunk_id")
        file_id = "-".join(chunk_id.split("-")[0:-1])
        chunk_type = kwargs.get("chunk_type")
        try:
            self.__requests[file_id][chunk_type] = True
        except Exception as e:
            print e
        self.__receive(file_id)

    def __get_file_size(self, file_size):
        return os.stat(file_size).st_size

    """
    def get_file_size(self, file_size):
        old_file_position = file_size.tell()
        file_size.seek(0, os.SEEK_END)
        size = file_size.tell()
        file_size.seek(old_file_position, os.SEEK_SET)
        return size
    """

    def get_north_backend(self):
        return self.__north_backend

    def get_south_backend(self):
        return self.__south_backend

    def get_west_backend(self):
        return self.__west_backend

    def get_east_backend(self):
        return self.__east_backend

    def disconnect(self):
        self.__north_backend.leave(self.__id)
        return True
