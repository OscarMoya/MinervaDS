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
        self.__configure()
        self.active_endpoints = list()

    def start(self):
        self.__south_backend.start()

    def __configure(self):
        self.__south_backend(self.__get_south_backend())
        self.__north_backend(self.__get_north_backend())

    def __get_north_backend(self):
        north_backend = ControllerNorthServer()
        return north_backend

    def __get_south_backend(self):
        pipe = self
        south_backend_driver = ControllerSouthDriver(pipe)
        south_backend_driver.set_file_db(DefaultFileDB())
        south_backend_driver.set_endpoint_db(DefaultEndPointDB())
        south_backend_driver.start() #Start DB

        south_backend = ControllerSouthAPI(south_backend_driver)

        return south_backend

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
        self.__remove_endpoint(self, kwargs.get("id"))

    def __process_read_request_event(self, **kwargs):
        #TODO probably just log the call
        pass

    def __process_write_request_event(self, **kwargs):
        #TODO probably just log the call
        pass

    def __add_endpoint(self, **kwargs):
        self.__active_endpoints[kwargs.get("id")] = {"type":kwargs.get("type"),
                                                     "url":kwargs.get("url"),
                                                     "data_ip": kwargs.get("data_ip")}

    def __remove_endpoint(self, id):
        self.active_endpoints.pop(id)

    def __mount_end_point(self, id):
        endpoint = self.__active_endpoints.get(id)
        mounted_endpoint = xmlrpclib.ServerProxy(endpoint.get("url"))
        return mounted_endpoint

