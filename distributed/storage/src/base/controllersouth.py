from abc import ABCMeta
from abc import abstractmethod

class ControllerSouthBase:

    __metaclass__ = ABCMeta

    @abstractmethod
    def ping(self):
        return

    @abstractmethod
    def syn_request(self):
        return


