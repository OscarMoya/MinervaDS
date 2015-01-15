from abc import ABCMeta
from abc import abstractmethod

class EndPointEastBase:

    __metaclass__ = ABCMeta

    @abstractmethod
    def ping(self, server_param):
        return

    @abstractmethod
    def read(self, client_id, file_id, server_param):
        return

    @abstractmethod
    def write(self, file_data, file_id, server_param):
        return

    @abstractmethod
    def syn(self):
        return
