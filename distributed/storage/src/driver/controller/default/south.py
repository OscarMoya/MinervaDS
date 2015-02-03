from distributed.storage.src.base.endpointnorth import EndPointNorthBase
from distributed.storage.src.config.config import DSConfig

from distributed.storage.lib.decorator.processoutput import processoutput

import uuid

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
        return result

    def read_request(self, client_id, file_id,):
        server_a = self.__file_db.filter(file_id=file_id, client_id=client_id, chunk_type=self.CHUNK_A_TYPE)[0]
        server_b = self.__file_db.filter(file_id=file_id, client_id=client_id, chunk_type=self.CHUNK_B_TYPE)[0]
        server_c = self.__file_db.filter(file_id=file_id, client_id=client_id, chunk_type=self.CHUNK_AXB_TYPE)[0]

        result = {self.CHUNK_A_TYPE: server_a.get("server_url"),
                  self.CHUNK_B_TYPE: server_b.get("server_url"),
                  self.CHUNK_AXB_TYPE:server_c.get("server_url")}

        self.__alert_pipe("read_request", client_id=client_id, file_id=file_id)
        return result

    def write_request(self, client_id, file_size, user_requirements):

        servers = self.__endpoint_db.filter(type=self.SERVER_TYPE)
        file_id = str(uuid.uuid4())
        #TODO: do the magic getting the most suitable servers :)

        #TODO: Solving things in ugly way when not enough servers
        if len(servers) < 3:
            servers = [servers[0],servers[0],servers[0]]
        server_a = servers[0]
        server_b = servers[1]
        server_c = servers[2]

        print servers[0]

        #XXX This should not be stored here
        self.__file_db.save(client_id=client_id, id=server_a.keys()[0], file_id=file_id, chunk_type=self.CHUNK_A_TYPE)
        self.__file_db.save(client_id=client_id, id=server_b.keys()[0], file_id=file_id, chunk_type=self.CHUNK_B_TYPE)
        self.__file_db.save(client_id=client_id, id=server_c.keys()[0], file_id=file_id, chunk_type=self.CHUNK_AXB_TYPE)

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
        return "dummy"#TODO implement
