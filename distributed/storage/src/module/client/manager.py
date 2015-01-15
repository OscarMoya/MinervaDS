
class ClientManager:

    def __init__(self):
        self.__north_backend = None
        self.__east_backend = None
        self.__south_backend = None

    def configure_client(self, mgmt_ip, mgmt_port, data_ip, data_port):
        self.__configure_east_backend(data_ip, data_port)
        self.__configure_south_backend(mgmt_ip, mgmt_port)

    def start(self):

        pass

    def upload_file(self, file, requirements):
        servers = self.__north_backend.write_request()

        pass

    def download_file(self):
        pass





