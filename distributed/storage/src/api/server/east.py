from distributed.storage.src.base.endpointeast import EndPointEastBase
import xmlrpclib

class ServerEastAPI(EndPointEastBase):
    """
    Client side, sender
    """

    def __init__(self):
        self.__server_east_channel = None

    def ping(self,):
        result = self.__server_east_channel.ping()
        return self.__process_result(result)

    def read(self, client_id, file_id):
        result = self.__server_east_channel.read(client_id, file_id)
        return self.__process_result(result)

    #TODO Remove server_param, add chunk_type
    def write(self, file_data, file_id, chunk_type):
        result = self.__server_east_channel.write(file_data, file_id,)
        return self.__process_result(result)

    def __initialize(self, ip, port):
        self.__server_east_channel = xmlrpclib.ServerProxy(ip, port)

    def __process_result(self, result):
        #TODO Do something. like raise exceptions if needed
        return result

    def get_server_east_channel(self):
        return self.__server_east_channel

    def set_server_east_ip(self, ip):
        self.__server_east_ip = ip

