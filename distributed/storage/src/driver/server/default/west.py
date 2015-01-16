from distributed.storage.src.base.endpointeast import EndPointEastBase
from distributed.storage.src.util.packetmanager import PacketManager

class ServerWestDriver(EndPointEastBase):

    def __init__(self, url=None, type=None):
        self.__url = None
        self.__type = None

    def ping(self):
        return "PONG"

    def syn_request(self):
        result = PacketManager.send_sync()
        return result

    def read(self, client_id, file_id):
        result = read_data(client_id, file_id)
        return result

    def write(self, file_data, file_id, chunk_type):
        result = write_data(file_data, file_id, chunk_type)
        return result
