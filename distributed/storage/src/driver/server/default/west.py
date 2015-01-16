from distributed.storage.src.base.endpointeast import EndPointEastBase
from distributed.storage.src.util.packetmanager import PacketManager

class ServerWestDriver(EndPointEastBase):

    def __init__(self, url=None, type=None):
        self.__url = None
        self.__data_db = None

    def ping(self):
        return "PONG"

    def syn_request(self):
        result = PacketManager.send_sync()
        return result

    def read(self, client_id, file_id):
        result = self.__data_db.filter(file_id=file_id, client_id=client_id)

        self.__alert_pipe(self.read, client_id=client_id, file_id=file_id)
        return result


    def write(self, file_data, file_id, chunk_type):
        self.__data_db.save(file_data=file_data, file_id=file_id)
        return
