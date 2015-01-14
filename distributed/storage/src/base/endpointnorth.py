from abc import ABCMeta
from abc import abstractmethod

class EndPointNorthBase:

    __metaclass__ == ABCMeta
    
    @abstractmethod
    def join(self, id, mgmt_ip, data_ip):
        return
    
    @abstractmethod
    def leave(self, id):
        return

    @abstractmethod
    def read_request(self, file_id):
        return

    @abstractmethod
    def write_request(self, file_size, user_requirements):
        return
