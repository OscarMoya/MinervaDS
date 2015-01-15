from abc import ABCMeta
from abc import abstractmethod

class DBBase:

    __metaclass__ == ABCMeta

    @abstractmethod
    def save(self, **kwargs):
        return

    @abstractmethod
    def load(self, **kwargs):
        return

    @abstractmethod
    def filter(self, **kwargs):
        return

    @abstractmethod
    def remove(self, **kwargs):
        return
