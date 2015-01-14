from distributed.storage.src.base.controllersouth import ServerBase
import binascii
import os
import socket
import SocketServer
import StringIO
import time
import threading


class UDPServer(ServerBase):
    """Not implemented yet"""
    def __init__(self):
        self.__db = None
        self.__address = None
        self.__port = None
        self.__type = None
        self.__name = None
        self.__handler = None
        self.__server = None


    def __server(self):
        pass


    def __handler(self, object):
        pass

    def read(self, db_id):




        pass

    def write(self, db_id, data):



        pass

    def ping(self): 



        pass

#########################################################################
if __name__ = "__main__":
    
    #def server(): as decorator function for UDP server class
    # handler to be called by server() on requests basis
    SERVER_IP = ""
    SERVER_PORT = 
    NAME = ""
    server = ThreadedUDPServer((SERVER_IP, SERVER_PORT), service_handler)
    server.allow_reuse_address = True
    ip, port = server.server_address
    buf = StringIO.StringIO()
    server_thread = threading.Thread(target=server.serve_forever, name=None, args=buf)
    
    server_thread.start()
    print "Starting %s in Thread: %s" % (NAME, server_thread.name)

