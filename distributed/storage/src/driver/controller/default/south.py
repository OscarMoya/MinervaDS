from distributed.storage.src.base.endpointnorth import EndPointNorthBase
from distributed.storage.src.config.config import DSConfig
import uuid

class ControllerSouthDriver(EndPointNorthBase):

    def __init__(self, db=None):
        self.__endpoint_db = None
        self.__file_db = None

        self.SERVER_TYPE = "server"
        self.CLIENT_TYPE = "client"

        self.CHUNK_A_TYPE = "A"
        self.CHUNK_B_TYPE = "B"
        self.CHUNK_AXB_TYPE = "AxC"

    def join(self, id, type, mgmt_ip, data_ip):
        url = "http://%s:%d" % (mgmt_ip, DSConfig.DEFAULT_MGMT_PORT)
        result = self.__db.save(id=id, type=type, url=mgmt_ip, data_ip=data_ip)
        return result

    def leave(self, id):
        result = self.__db.delete(id)
        return result

    def read_request(self, client_id, file_id,):
        server_a = self.__file_db.filter(file_id=file_id, client_id=client_id, chunk_type=self.CHUNK_A_TYPE)[0]
        server_b = self.__file_db.filter(file_id=file_id, client_id=client_id, chunk_type=self.CHUNK_B_TYPE)[0]
        server_c = self.__file_db.filter(file_id=file_id, client_id=client_id, chunk_type=self.CHUNK_AXB_TYPE)[0]

        result = {"A": server_a.get("server_url"),
                  "B": server_b.get("server_url"),
                  "AxB":server_c.get("server_url")}

        return result

    def write_request(self,client_id, file_size, user_requirements):
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
                  "server_a": server_a.get("url"),
                  "server_b": server_b.get("url"),
                  "server_c": server_c.get("url"),}

        return result

    def start(self):
        self.__endpoint_db.load()
        self.__file_db.load()