from abc import ABCMeta
from abc import abstractmethod

class DBBase:

    __metaclass__ == ABCMeta

    @abstractmethod
    def save(self):
        return

    @abstractmethod
    def load(self):
        return 
