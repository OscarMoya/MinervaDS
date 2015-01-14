from distributed.storage.src.base.endpointnorth import EndPointNorthBase
import xmlrpclib

class ClientNorthAPI(EndPointNorthBase):

    def __init__(self):
        self.__controller_north_channel = None

    def join(self, client_id, mgmt_ip, data_ip):
        result = self.__controller_north_channel.join(client_id, mgmt_ip, data_ip)
        return self.__process_result(result)

    def leave(self, client_id):
        result = self.__controller_north_channel.leave(client_id)
        return

    def read_request(self, client_id, file_id):
        result = self.__controller_north_channel.read_request(client_id, file_id)
        return

    def write_request(self, file_size, user_requirements):
        result = self.__controller_north_channel.write_request(file_size, user_requirements)
        return

    def __initialize(self, ip, port):
        self.__controller_north_channel = xmlrpclib.ServerProxy(ip, port)

    def __process_result(self, result):
        #TODO Do something. like raise exceptions if needed
        return result

    def get_controller_north_channel(self):
        return self.__controller_north_channel

    def set_controller_north_ip(self, ip):
        self.__controller_north_ip = ip

