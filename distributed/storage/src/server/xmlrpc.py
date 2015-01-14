from distributed.storage.src.base.controllersouth import ServerBase
from SimpleXMLRPCServer import SimpleXMLRPCServer
import xmlrpclib



class XmlRpcServer(ServerBase):

    def __init__(self):
        self.__db = None
        self.__address = None
        self.__type = None
        self.__name = None
        self.__server()

    def __server(self):
        pass

    def read(self, db_id):
        print "SERVER %s: Reading file with ID %d" % (self.__name, db_id)
        f = open("/home/pox/apps/flow"+self.__name+"/" + str(db_id),"r+")
        data = f.read()
        f.close()
        return data

    def write(self, db_id, data):
        print "%s: Reading file with ID %d" % (self.__name, db_id)
        f = open("/home/pox/apps/flow"+self.__name+"/" + str(db_id), "w+")
        f.write(data)
        f.close()
        return "SERVER %s: Data correctly saved"
        

    def ping(self): 
        print "Ping received in %s" % self.__name       
        return "Pong %s" % self.__name
       
