from SimpleXMLRPCServer import SimpleXMLRPCServer
from distributed.storage.src.base.controllersouth import ControllerSouthBase
from distributed.storage.src.util.threadmanager import ThreadManager

class ClientSouthServer(ControllerSouthBase):
    def ping(self):
        return "PONG"

    def syn_request(self):
        return True

class ClientSouthServerHandler:

    def __init__(self):
        self.__server = None

    def set_up_server(self, ip, port):
        self.__server = SimpleXMLRPCServer((ip, port))
        self.__server.register_instance(ClientSouthServer())
        return True

    def start_server(self):
        self.__server.serve_forever()
        return True

class ClientSouthAPI(ControllerSouthBase):

    def __init__(self):
        self.__handler = ClientSouthServerHandler()

    def start_api(self, ip, port):
        self.__handler.set_up_server(ip, port)
        ThreadManager.start_method_in_new_thread(self.__handler.start_server, [])
        return True

