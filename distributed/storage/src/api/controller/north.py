from distributed.storage.src.base.controllersouth import ControllerSouthBase
import xmlrpclib

class ControllerNorthServer(ControllerSouthBase):

    def __init__(self):
        self.__server = None

    def ping(self):
        result = self.__server.ping()
        return self.__process_result(result)

    def req_response(self):
        """
        Controller message sent to Client to confirm a REQ
        reception on Controller from Client
        """
        result = self.__server.true_response()
        return self.__process_result(result)

    def syn_request(self):
        result = self.__server.syn_request()
        return self.__process_result(result)

    def initialize(self, ip, port):
        self.__server = xmlrpclib.ServerProxy(ip, port)
        return True

    def __process_result(self, result):
        return result


