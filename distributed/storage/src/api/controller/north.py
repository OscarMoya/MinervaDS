from distributed.storage.src.base.controllersouth import ControllerSouthBase
import xmlrpclib

class ControllerNorthServer(ControllerSouthBase):

    def __init__(self):
        self.__server = None
        pass

    def ping(self):
        result = self.__server.ping()
        return self.__process_result(result)

    def syn_request(self):
        result = self.__server.syn_request()
        return self.__process_result(result)

    def initialize(self, ip, port):
        self.__server = xmlrpclib.ServerProxy(ip, port)
        return True

    def __process_result(self, result):
        return result


