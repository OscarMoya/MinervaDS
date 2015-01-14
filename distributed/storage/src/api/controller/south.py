from distributed.storage.src.base.endpointnorth import EndPointNorthBase
from distributed.storage.src.util.threadmanager import ThreadManager
import xmlrpclib

class ControllerSouthServer(EndPointNorthBase):

    def __init__(self, driver):
        self.__driver = driver

    def join(self, client_id, mgmt_ip, data_ip):
        return self.__driver.join(client_id, mgmt_ip, data_ip)

    def leave(self, client_id):
        return  self.__driver.leave()

    def read_request(self, client_id, file_id):
        return self.__driver.read_request(client_id, file_id)

    def write_request(self, file_size, user_requirements):
        return self.__driver.write_request(file_size, user_requirements)

    def initialize(self, ip, port):
        self.__controller_north_channel = xmlrpclib.ServerProxy(ip, port)

class ControllerSouthServerHandler:

    def __init__(self, driver):
        self.__server = None
        self.__driver = driver

    def set_up_server(self, ip, port):
        self.__server = xmlrpclib.SimpleXMLRPCServer((ip, port))
        self.__server.register_instance(ControllerSouthServer(self.__driver))
        return True

    def start_server(self):
        self.__server.serve_forever()
        return True

class ControllerSouthAPI():

    def __init__(self, driver):
        self.__handler = ClientSouthServerHandler(driver)

    def start_api(self, ip, port):
        self.__handler.set_up_server(ip, port)
        ThreadManager.start_method_in_new_thread(self.__handler.start_server, [])
        return True