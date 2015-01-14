from abc import ABCMeta
from abc import abstractmethod

class EndPointEastBase:

    __metaclass__ == ABCMeta

    @abstractmethod
    def ping(self):
        return

    @abstractmethod
    def read(self, file_id):
        return

    @abstractmethod
    def write(self, file, file_id):
        return

    @abstractmethod
    def syn(self):
        return
