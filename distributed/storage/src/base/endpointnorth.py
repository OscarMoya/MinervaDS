from abc import ABCMeta
from abc import abstractmethod

class EndPointNorthBase:

    __metaclass__ = ABCMeta
    
    @abstractmethod
    def join(self, client_id, type, mgmt_ip, data_ip):
        return
    
    @abstractmethod
    def leave(self, id):
        return

    @abstractmethod
    def read_request(self, client_id, file_id):
        return

    @abstractmethod
    def write_request(self, client_id, file_size, user_requirements):
        return
