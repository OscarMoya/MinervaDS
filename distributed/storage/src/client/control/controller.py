from distributed.storage.src.base.endpointeast import ControlBase
import xmlrpclib

class Controller(ControlBase):

    def __init__(self):
        self.__controller_url = None
        self.__controller_port = None
        self.__controller_channel = None

    def read_request(self, db_id):
        """
        :param db_id: id to identify the file that is going to be read
        :return: Triple of tuples containing the ip and port of the servers
        """
        return self.__controller_channel.read_request(db_id)

    def write_request(self, file_size, with_reliable_connection=True):
        """
        :param file_size: size of the file to be stored
        :param with_reliable_connection: Flag requesting for reliable connections
        :return: Structure with the 3 servers, dbid and driver
        """
        return self.__controller_channel.write_request(file_size, with_reliable_connection)

    def connect(self, url, port):
        self.__controller_channel = xmlrpclib.ServerProxy(url, port)

    def get_controller_url(self):
        return self.__controller_url

    def set_controller(self, controller):
        self.__controller_url = controller



