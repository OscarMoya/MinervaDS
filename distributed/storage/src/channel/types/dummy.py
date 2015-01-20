from distributed.storage.src.base.endpointeast import EndPointEastBase
import xmlrpclib

class DummyChannel(EndPointEastBase):

    def __init__(self, url=None):
        self.__url = url
        self.__medium = None

    def ping(self):
        return self.__medium.ping()

    def read(self, client_id, file_id):
        return self.__medium.read(file_id)

    def write(self, file_data, file_id, chunk_type):
        return self.__medium.write(file_data, file_id)

    def get_url(self):
        return self.__url

    def set_url(self, url):
        return url

    def start(self):
        self.__medium = xmlrpclib.ServerProxy(self.__url)

def launch():
    return DummyChannel
