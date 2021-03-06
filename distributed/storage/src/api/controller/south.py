from distributed.storage.src.base.endpointnorth import EndPointNorthBase
from distributed.storage.src.util.threadmanager import ThreadManager
from SimpleXMLRPCServer import SimpleXMLRPCServer
import xmlrpclib

class ControllerSouthServer(EndPointNorthBase):

    def __init__(self, driver):
        self.__driver = driver

    def join(self, client_id, type, mgmt_ip, data_ip):
        return self.__driver.join(client_id, type, mgmt_ip, data_ip)

    def leave(self, client_id):
        return self.__driver.leave(client_id)

    def read_request(self, client_id, file_id):
        return self.__driver.read_request(client_id, file_id)

    def write_request(self, client_id, file_size, user_requirements):
        return self.__driver.write_request(client_id, file_size, user_requirements)

    def ping(self):
        return self.__driver.ping()


class ControllerSouthServerHandler:

    def __init__(self, driver):
        self.__server = None
        self.__driver = driver

    def set_up_server(self, ip, port):
        self.__server = SimpleXMLRPCServer((ip, port))
        self.__server.register_instance(ControllerSouthServer(self.__driver))
        self.__server.register_function(self.stop_server)
        return True

    def start_server(self):
        self.__server.serve_forever()
        return True

    def stop_server(self):
        return self.__server.shutdown()


class ControllerSouthAPI:

    def __init__(self, driver):
        self.__handler = ControllerSouthServerHandler(driver)

    def start(self, ip, port):
        self.__handler.set_up_server(ip, port)
        ThreadManager.start_method_in_new_thread(self.__handler.start_server, [],name="Controller south on: " +ip+":"+str(port))
        return True