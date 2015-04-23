from distributed.storage.src.base.endpointeast import EndPointEastBase
import xmlrpclib

class DummyChannel(EndPointEastBase):

    def __init__(self, url=None, client=None):
        self.__url = url
        self.__medium = None
        self.__client = client

    def ping(self):
        return self.__medium.ping()

    def read(self, client_id, file_id):
        return self.__medium.read(file_id)

    def write(self, file_data, file_id, chunk_type):
        try:
            return self.__medium.write(file_data, file_id, chunk_type)
        except Exception as e:
            print e

    def syn(self):
        pass

    def get_url(self):
        return self.__url

    def set_url(self, url):
        return url

    def start(self):
        self.__medium = xmlrpclib.ServerProxy(self.__url)


def launch():
    return DummyChannel
