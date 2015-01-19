from distributed.storage.src.base.endpointeast import EndPointEastBase
from distributed.storage.src.util.threadmanager import ThreadManager
from SimpleXMLRPCServer import SimpleXMLRPCServer
import xmlrpclib


class ServerWestServer(EndPointEastBase):

    def __init__(self, driver):
        self.__driver = driver

    def ping(self, server_param):
        return self.__driver.ping()

    def syn(self):
        return self.__driver.send_sync()

    def read(self, client_id, file_id, server_param):
        return self.__driver.read_data()

    def write(self, file_data, file_id, server_param):
        return self.__driver.write_data()

class ServerWestServerHandler:

    def __init__(self, driver):
        self.__server = None
        self.__driver = driver

    def set_up_server(self, ip, port):
        self.__server = SimpleXMLRPCServer((ip, port))
        self.__server.register_instance(ServerWestServer(self.__driver))
        return True

    def start_server(self):
        self.__server.serve_forever()
        return True

class ServerWestAPI(EndPointEastBase):

    def __init__(self, driver):
        self.__handler = ServerWestServerHandler(driver)

    def start_api(self, ip, port):
        self.__handler.set_up_server(ip, port)
        ThreadManager.start_method_in_new_thread(self.__handler.start_server, [])
        return True