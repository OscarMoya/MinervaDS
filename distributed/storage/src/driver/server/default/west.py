from distributed.storage.src.base.endpointeast import EndPointEastBase

class ServerWestDriver(EndPointEastBase):

    def __init__(self, db=None, pipe=None):
        self.__data_db = db
        self.__pipe = pipe
        self.__buffer = dict()

    def ping(self):
        self.__alert_pipe(self.ping)
        return "PONG"

    def syn(self):
        pass

    def read(self, client_id, file_id):
        result = self.__data_db.filter(file_id=file_id, client_id=client_id)
        self.__alert_pipe("read", client_id=client_id, file_id=file_id)
        return result

    def write(self, file_data, file_id, chunk_type):
        chunk_id = file_id + "-" + chunk_type
        result = self.__data_db.save(file_data=file_data, file_id=file_id, chunk_type=chunk_type, chunk_id=chunk_id)
        self.__alert_pipe("write", file_id=file_id, chunk_type=chunk_type, chunk_id=chunk_id)
        return result

    def __alert_pipe(self, func, **kwargs):
        if self.__pipe:
            return self.__pipe.alert(func, **kwargs)
