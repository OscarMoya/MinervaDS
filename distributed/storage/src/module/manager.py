class ServerManager:

    def __init__(self, db=None, id=None):
        if not id:
            id = uuid.uuid4()

        self.__nf_manager = None

        self.__type = DSConfig.SERVER_TYPE
        self.__default_mgmt_port = DSConfig.DEFAULT_MGMT_PORT
        self.__default_data_port = DSConfig.DEFAULT_DATA_PORT

        self.__north_backend = None
        self.__east_backend = None
        self.__west_backend = None
        self.__south_backend = None

        self.__id = id
        self.__db = db

        self.configure()

    def configure(self):
        self.__configure_west_backend()
        self.__configure_south_backend()
        self.__configure_north_backend()

    def __configure_west_backend(self):
        pass

    def __configure_south_backend(self):
        pass

    def __configure_north_backend(self):
        pass

    def start(self, mgmt_ip, mgmt_port, data_ip, data_port):
        self.__south_backend.start(mgmt_ip, mgmt_port)
        self.__west_backend.start(data_ip, data_port)
        self.__db.load_all()
        self.__north_backend.join(self.__id, self.__type, mgmt_ip, data_ip)

    def alert(self, func, **kwargs):
        pass

    def __process_write(self, **kwargs):
        pass

    def __process_ping(self, **kwargs):
        pass

    def send_to(self, file_id, endpoint_params):
        pass
    

