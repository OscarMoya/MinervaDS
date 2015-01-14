import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer

def ping():
    print "Ping Received in SERVER B"
    return "Pong_B"

def read(db_id):
    print "Server B: Reading file with ID %d" % db_id
    f = open("/home/pox/apps/flowB/" + str(db_id), "r+")
    data = f.read()
    f.close()
    return data

def write(data, db_id):
    print "Server B: writing file with ID %d" % db_id
    f = open("/home/pox/apps/flowB/" + str(db_id), "w+")
    f.write(data)
    f.close()
    return "SERVER B: Data Correctly Saved"


server = SimpleXMLRPCServer(("127.0.0.1", 9696))
server.register_function(ping, "ping")
server.register_function(read, "read")
server.register_function(write, "write")
print "starting server B..."
server.serve_forever()    
