from distributed.storage.src.base.endpointnorth import EndPointNorthBase
import xmlrpclib

class ServerNorthAPI(EndPointNorthBase):

    def __init__(self, channel=None):
        self.__controller_north_channel = channel

    def join(self, endpoint_id, type, mgmt_ip, data_ip):
        result = self.__controller_north_channel.join(endpoint_id, type, mgmt_ip, data_ip)
        return self.__process_result(result)

    def leave(self, endpoint_id):
        result = self.__controller_north_channel.leave(endpoint_id)
        return self.__process_result(result)

    def read_request(self, endpoint_id, file_id):
        result = self.__controller_north_channel.read_request(endpoint_id, file_id)
        return self.__process_result(result)

    def write_request(self, endpoint_id, file_size, user_requirements):
        result = self.__controller_north_channel.write_request(endpoint_id, file_size, user_requirements)
        return self.__process_result(result)

    def start(self, url):
        self.__controller_north_channel = xmlrpclib.ServerProxy(url)

    def __process_result(self, result):
        # TODO: Raise exception or similar if needed
        return result

    def get_controller_north_channel(self):
        return self.__controller_north_channel

    def set_controller_north_channel(self, channel):
        self.__controller_north_channel = channel
