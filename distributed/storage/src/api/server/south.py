from SimpleXMLRPCServer import SimpleXMLRPCServer
from distributed.storage.src.base.controllersouth import ControllerSouthBase
from distributed.storage.src.util.threadmanager import ThreadManager

class ServerSouthServer(ControllerSouthBase):

    def __init__(self, driver):
        self.__driver = driver

    def ping(self):
        return self.__driver.ping()

    def syn_request(self):
        return self.__driver.syn_request()

class ServerSouthServerHandler:

    def __init__(self, driver):
        self.__server = None
        self.__driver = driver

    def set_up_server(self, ip, port):
        self.__server = SimpleXMLRPCServer((ip, port))
        self.__server.register_instance(ServerSouthServer(self.__driver))
        return True

    def start_server(self):
        self.__server.serve_forever()
        return True


class ServerSouthAPI:

    def __init__(self, driver):
        self.__handler = ServerSouthServerHandler(driver)

    def start(self, ip, port):
        self.__handler.set_up_server(ip, port)
        ThreadManager.start_method_in_new_thread(self.__handler.start_server, [],name=ip+":"+str(port))
        return True
