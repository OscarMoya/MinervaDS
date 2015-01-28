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
    def join(self, id, type, mgmt_ip, data_ip):
        url = "http://%s:%d" % (mgmt_ip, DSConfig.DEFAULT_MGMT_PORT)
        result = self.__endpoint_db.save(id=id, type=type, url=mgmt_ip, data_ip=data_ip)
        self.__alert_pipe(self.join, id=id, type=type, url=url, data_ip=data_ip)
        return result

    @processoutput
    def leave(self, id):
        result = self.__endpoint_db.remove(id)
        self.__alert_pipe(self.leave, id=id)
        return result

    def read_request(self, client_id, file_id,):
        server_a = self.__file_db.filter(file_id=file_id, client_id=client_id, chunk_type=self.CHUNK_A_TYPE)[0]
        server_b = self.__file_db.filter(file_id=file_id, client_id=client_id, chunk_type=self.CHUNK_B_TYPE)[0]
        server_c = self.__file_db.filter(file_id=file_id, client_id=client_id, chunk_type=self.CHUNK_AXB_TYPE)[0]

        result = {self.CHUNK_A_TYPE: server_a.get("server_url"),
                  self.CHUNK_B_TYPE: server_b.get("server_url"),
                  self.CHUNK_AXB_TYPE:server_c.get("server_url")}

        self.__alert_pipe(self.read_request, client_id=client_id, file_id=file_id)
        return result

    def write_request(self, client_id, file_size, user_requirements):
        servers = self.__endpoint_db.filter(type=self.SERVER_TYPE)
        file_id = uuid.uuid4()
        #TODO: do the magic getting the most suitable servers :)

        server_a = servers[0]
        server_b = servers[1]
        server_c = servers[2]

        #XXX This should not be stored here
        self.__file_db.save(client_id=client_id, server_id=server_a.get("id"), file_id=file_id, chunk_type=self.CHUNK_A_TYPE)
        self.__file_db.save(client_id=client_id, server_id=server_b.get("id"), file_id=file_id, chunk_type=self.CHUNK_B_TYPE)
        self.__file_db.save(client_id=client_id, server_id=server_c.get("id"), file_id=file_id, chunk_type=self.CHUNK_AXB_TYPE)

        result = {"file_id": file_id,
                  self.CHUNK_A_TYPE: server_a.get("server_url"),
                  self.CHUNK_B_TYPE: server_b.get("server_url"),
                  self.CHUNK_AXB_TYPE: server_c.get("server_url"), }

        self.__alert_pipe(self.write_request, client_id=client_id, file_id=file_id)
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
            return self.__pipe.alert(func, kwargs)
