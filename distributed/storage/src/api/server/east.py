from distributed.storage.src.base.endpointeast import EndPointEastBase
import xmlrpclib

class ServerEastAPI(EndPointEastBase):

    def __init__(self):
        self.__server_east_channel = None

    def ping(self):
        #result = self.__controller_north_channel.leave(client_id)
        return

    def read(self, file_id):
        #result = self.__controller_north_channel.read_request(client_id, file_id)
        return

    def write(self, file_size, user_requirements):
        #result = self.__controller_north_channel.write_request(file_size, user_requirements)
        return

    def __initialize(self, ip, port):
        self.__server_east_channel = xmlrpclib.ServerProxy(ip, port)

    def __process_result(self, result):
        #TODO Do something. like raise exceptions if needed
        return result

    def get_server_east_channel(self):
        return self.__server_east_channel

    def set_server_east_ip(self, ip):
        self.__server_east_ip = ip

