from distributed.storage.src.base.endpointeast import EndPointEastBase
from distributed.storage.src.util.packetmanager import PacketManager

class ClientWestDriver(EndPointEastBase):

    def __init__(self, db=None, pipe=None):
        self.__data_db = db
        self.__pipe = pipe
        self.__buffer = dict()

    def ping(self):
        self.__alert_pipe("ping")
        return "PONG"

    def syn(self):
        pass

    def read(self, client_id, file_id):
        result = self.__data_db.filter(file_id=file_id, client_id=client_id)
        self.__alert_pipe("read", client_id=client_id, file_id=file_id)
        return result

    def write(self, file_data, chunk_type, chunk_id):
        file_id = "-".join(chunk_id.split("-")[0:-1])
        result = self.__data_db.save(file_data=file_data, chunk_id=chunk_id, chunk_type=chunk_type, file_id=file_id)
        self.__alert_pipe("write", file_data=file_data, chunk_type=chunk_type, chunk_id=chunk_id)
        return True

    def __alert_pipe(self, func, **kwargs):

        if self.__pipe:
            self.__pipe.alert(func, **kwargs)