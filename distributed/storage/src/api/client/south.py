from SimpleXMLRPCServer import SimpleXMLRPCServer
from distributed.storage.src.base.controllersouth import ControllerSouthBase
from distributed.storage.src.util.threadmanager import ThreadManager

class ClientSouthServer(ControllerSouthBase):

    def __init__(self, driver):
        self.__driver = driver

    def ping(self):
        return self.__driver.ping()

    def syn_request(self):
        return self.__driver.send_sync()


class ClientSouthServerHandler:

    def __init__(self, driver):
        self.__server = None
        self.__driver = driver

    def set_up_server(self, ip, port):
        self.__server = SimpleXMLRPCServer((ip, port))
        self.__server.register_instance(ClientSouthServer(self.__driver))
        return True

    def start_server(self):
        self.__server.serve_forever()
        return True


class ClientSouthAPI:

    def __init__(self, driver):
        self.__handler = ClientSouthServerHandler(driver)

    def start(self, ip, port):
        self.__handler.set_up_server(ip, port)
        ThreadManager.start_method_in_new_thread(self.__handler.start_server, [])
        return True

