from distributed.storage.src.base.endpointeast import EndPointEastBase
from distributed.storage.src.util.threadmanager import ThreadManager
from SimpleXMLRPCServer import SimpleXMLRPCServer

class ClientWestServer(EndPointEastBase):
    """
    Client-server side, receiver
    """

    def __init__(self, driver):
        self.__driver = driver

    def ping(self):
        return self.__driver.ping()

    def syn(self):
        return self.__driver.syn()

    def read(self, client_id, file_id):
        return self.__driver.read_data()

    def write(self, file_data, file_id, chunk_type):
        return self.__driver.write_data()


class ClientWestServerHandler:

    def __init__(self, driver):
        self.__client = None
        self.__driver = driver

    def set_up_client(self, ip, port):
        self.__client = SimpleXMLRPCServer((ip, port))
        self.__client.register_instance(ClientWestServer(self.__driver))
        return True

    def start_client(self):
        self.__client.serve_forever()
        return True


class ClientWestAPI:

    def __init__(self, driver):
        self.__handler = ClientWestServerHandler(driver)

    def start(self, ip, port):
        self.__handler.set_up_client(ip, port)
        ThreadManager.start_method_in_new_thread(self.__handler.start_client, [], name="ClientWest-"+ip+":"+str(port))
        return True