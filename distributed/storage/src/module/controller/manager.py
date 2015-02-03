from distributed.storage.src.driver.controller.default.south import ControllerSouthDriver
from distributed.storage.src.api.controller.north import ControllerNorthServer
from distributed.storage.src.api.controller.south import ControllerSouthAPI
from distributed.storage.src.driver.db.file.default import DefaultFileDB
from distributed.storage.src.driver.db.endpoint.default import DefaultEndPointDB

import xmlrpclib
from distributed.storage.src.util.threadmanager import ThreadManager


class ControllerManager:

    def __init__(self):
        self.__south_backend = None
        self.__north_backend = None
        self.configure()
        self.active_endpoints = dict()

    def start(self, mgmt_ip, mgmt_port):
        self.__south_backend.start(mgmt_ip, mgmt_port)

    def configure(self):
        self.__configure_south_backend()


    def __configure_south_backend(self):
        self.__south_backend = self.__get_south_backend()


    def __get_south_backend(self):
        pipe = self
        e_db = DefaultEndPointDB()
        f_db = DefaultFileDB()
        south_backend_driver = ControllerSouthDriver(endpoint_db=e_db, pipe=pipe, file_db=f_db)
        api = ControllerSouthAPI(south_backend_driver)
        self.__south_backend = api
        return self.__south_backend

    def alert(self, func, **kwargs):
        if func == "join":
            self.__process_join_event(**kwargs)
        elif func == "leave":
            self.__process_leave_event(**kwargs)
        elif func == "read_request":
            self.__process_read_request_event(**kwargs)
        elif func == "write_request":
            self.__process_write_request_event(**kwargs)
        else:
            #TODO See what we can do
            pass

    def __process_join_event(self, **kwargs):
        self.__add_endpoint(**kwargs)
        endpoint = self.__mount_endpoint(kwargs.get("id"), "mgmt")
        ThreadManager.start_method_in_new_thread(endpoint.syn_request, [], name=kwargs.get("id"))

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
                                                     "data_url": kwargs.get("data_url"),
                                                     "mgmt_url": kwargs.get("mgmt_url")}

    def __remove_endpoint(self, id):
        self.active_endpoints.pop(id)

    def __mount_endpoint(self, id, type):

        endpoint = self.active_endpoints.get(id)
        mounted_endpoint = xmlrpclib.ServerProxy(endpoint.get("%s_url" % type))
        return mounted_endpoint

    def get_south_backend(self):
        return self.__south_backend
