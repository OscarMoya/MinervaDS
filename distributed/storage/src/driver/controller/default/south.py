import xmlrpclib
from distributed.storage.src.base.endpointnorth import EndPointNorthBase
from distributed.storage.src.config.config import DSConfig

from distributed.storage.lib.decorator.processoutput import processoutput

import uuid
from distributed.storage.src.util.threadmanager import ThreadManager


class ControllerSouthDriver(EndPointNorthBase):

    def __init__(self, pipe=None, endpoint_db=None, file_db=None):
        self.__endpoint_db = endpoint_db
        self.__file_db = file_db
        self.__pipe = pipe

        self.SERVER_TYPE = "server"
        self.CLIENT_TYPE = "client"

        self.CHUNK_A_TYPE = "A"
        self.CHUNK_B_TYPE = "B"
        self.CHUNK_AXB_TYPE = "AxB"

    @processoutput
    def ping(self):
        return "Pong"

    @processoutput
    def join(self, id, type, mgmt_url, data_url):
        result = self.__endpoint_db.save(id=id, type=type, mgmt_url=mgmt_url, data_url=data_url)
        self.__alert_pipe("join", id=id, type=type, mgmt_url=mgmt_url, data_url=data_url)
        return result

    @processoutput
    def leave(self, id):
        result = self.__endpoint_db.remove(id=id)
        self.__alert_pipe("leave", id=id)
        return True

    def read_request(self, client_id, file_id):


        result = {self.CHUNK_A_TYPE: file_id,
                  self.CHUNK_B_TYPE: file_id,
                  self.CHUNK_AXB_TYPE:file_id}

        ThreadManager.start_method_in_new_thread(self.__alert_wrap, ["read_request", client_id, file_id])
        return result

    def write_request(self, client_id, file_size, user_requirements):
        try:
            servers = self.__endpoint_db.filter(type=self.SERVER_TYPE)
        except Exception as e:
            raise e

        file_id = str(uuid.uuid4())
        #TODO: do the magic getting the most suitable servers :)

        #TODO: Solving things in ugly way when not enough servers
        if len(servers) < 3:
            servers = [servers[0],servers[0],servers[0]]
        server_a = servers[0]
        server_b = servers[1]
        server_c = servers[2]

        #XXX This should not be stored here
        self.__file_db.save(chunk_id=file_id+"-"+self.CHUNK_A_TYPE, client_id=client_id, server_id=server_a.keys()[0], file_id=file_id, chunk_type=self.CHUNK_A_TYPE)
        self.__file_db.save(chunk_id=file_id+"-"+self.CHUNK_B_TYPE, client_id=client_id, server_id=server_b.keys()[0], file_id=file_id, chunk_type=self.CHUNK_B_TYPE)
        self.__file_db.save(chunk_id=file_id+"-"+self.CHUNK_AXB_TYPE, client_id=client_id, server_id=server_c.keys()[0], file_id=file_id, chunk_type=self.CHUNK_AXB_TYPE)

        channel = self.__get_channel(user_requirements)

        result = {"file_id": file_id,
                  "channel": channel,
                  self.CHUNK_A_TYPE: server_a.get(server_a.keys()[0]).get("data_url"),
                  self.CHUNK_B_TYPE: server_b.get(server_b.keys()[0]).get("data_url"),
                  self.CHUNK_AXB_TYPE: server_c.get(server_c.keys()[0]).get("data_url"),}

        self.__alert_pipe("write_request", client_id=client_id, file_id=file_id)
        return result

    def start(self):
        self.__endpoint_db.load()
        self.__file_db.load()

    def get_file_db(self):
        return self.__file_db

    def get_endpoint_db(self):
        return self.__endpoint_db

    def set_file_db(self, db):
        self.__file_db = db

    def set_endpoint_db(self, db):
        self.__endpoint_db = db

    def __alert_pipe(self, func, **kwargs):
        if self.__pipe:
            return self.__pipe.alert(func, **kwargs)

    def __get_channel(self, requirements):
        return "dummy" #TODO implement

    def __mount_server(self, url):
        return xmlrpclib.ServerProxy(url)

    def __alert_wrap(self, method, client_id, file_id):
        self.__alert_pipe(method, client_id=client_id, file_id=file_id)

