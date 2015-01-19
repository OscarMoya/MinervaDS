from distributed.storage.src.base.endpointeast import EndPointEastBase
import xmlrpclib

class DummyChannel(EndPointEastBase):

    def __init__(self, url=None):
        self.__url = url
        self.__medium = None

    def ping(self):
        return self.__client.ping()

    def read(self, file_id):
        return self.__client.read(file_id)

    def write(self, file, file_id):
        return self.__client.write(file, file_id)

    def get_url(self):
        return self.__url

    def set_url(self, url):
        return url

    def start(self):
        self.__medium = xmlrpclib.ServerProxy(self.__url)

def launch():
    return DummyChannel