from abc import ABCMeta
from abc import abstractmethod

class EndPointEastBase:

    __metaclass__ = ABCMeta

    @abstractmethod
    def ping(self,):
        return

    @abstractmethod
    def read(self, client_id, file_id):
        return

    @abstractmethod
    def write(self, file_data, file_id, chunk_type):
        return

    @abstractmethod
    def syn(self):
        return
