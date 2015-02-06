from distributed.storage.src.base.endpointeast import EndPointEastBase
import xmlrpclib

class ClientEastAPI(EndPointEastBase):
    """
    Client-client side, sender
    """

    def __init__(self):
        self.__client_east_channel = None
        self.__client_east_ip = None

    def ping(self,):
        result = self.__client_east_channel.ping()
        return self.__process_result(result)

    def read(self, client_id, file_id):
        result = self.__client_east_channel.read(client_id, file_id)
        return self.__process_result(result)

    def write(self, file_data, file_id, chunk_type):
        result = self.__client_east_channel.write(file_data, file_id, chunk_type)
        return self.__process_result(result)

    def __start(self, ip, port):
        self.__client_east_channel = xmlrpclib.ServerProxy(ip, port)

    def __process_result(self, result):
        #TODO Do something. like raise exceptions if needed
        return result

    def get_client_east_channel(self):
        return self.__client_east_channel

    def set_client_east_ip(self, ip):
        self.__client_east_ip = ip

