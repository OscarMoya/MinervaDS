from distributed.storage.src.driver.controller.default.south import ControllerSouthDriver
from distributed.storage.src.api.controller.north import ControllerNorthServer
from distributed.storage.src.api.controller.south import ControllerSouthAPI
from distributed.storage.src.driver.db.file.default import DefaultFileDB
from distributed.storage.src.driver.db.endpoint.default import DefaultEndPointDB

import xmlrpclib

class ControllerManager:

    def __init__(self):
        self.__south_backend = None
        self.__north_backend = None
        self.configure()
        self.active_endpoints = dict()

    def start(self, mgmt_ip, mgmt_port):
        #
        self.__south_backend.start(mgmt_ip, mgmt_port)

    def configure(self):
        self.__configure_south_backend()
        self.__configure_north_backend()

    def __configure_north_backend(self):
        self.__north_backend = self.__get_north_backend()

    def __configure_south_backend(self):
        self.__south_backend = self.__get_south_backend()

    def __get_north_backend(self):
        #TODO: Fix it
        north_backend = ControllerNorthServer()

        return north_backend

    def __get_south_backend(self):
        #

        pipe = self
        db = DefaultEndPointDB()
        south_backend_driver = ControllerSouthDriver(db, pipe)
        api = ControllerSouthAPI(south_backend_driver)
        self.__south_backend = api
        return self.__south_backend

    def alert(self, func, **kwargs):
        if func.__name__ == "join":
            self.__process_join_event(**kwargs)
        elif func.__name__ == "leave":
            self.__process_leave_event(**kwargs)
        elif func.__name__ == "read_request":
            self.__process_read_request_event(**kwargs)
        elif func.__name__ == "write_request":
            self.__process_write_request_event(**kwargs)
        else:
            #TODO See what we can do
            pass

    def __process_join_event(self, **kwargs):
        self.__add_endpoint(self, **kwargs)
        endpoint = self.__mount_endpoint(kwargs.get("id"))
        endpoint.send_sync()

    def __process_leave_event(self, **kwargs):
        self.__remove_endpoint(kwargs.get("id"))

    def __process_read_request_event(self, **kwargs):
        #TODO probably just log the call
        pass

    def __process_write_request_event(self, **kwargs):
        #TODO probably just log the call
        pass

    def __add_endpoint(self, **kwargs):
        self.active_endpoints[kwargs.get("id")] = {"type": kwargs.get("type"),
                                                     "url": kwargs.get("url"),
                                                     "data_ip": kwargs.get("data_ip")}

    def __remove_endpoint(self, id):
        self.active_endpoints.pop(id)

    def __mount_endpoint(self, id):
        endpoint = self.active_endpoints.get(id)
        mounted_endpoint = xmlrpclib.ServerProxy("http://"+endpoint.get("url"))
        return mounted_endpoint
