import binascii
import random
import sys
import xmlrpclib
import socket

class mcolors:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.OKGREEN = ''
        self.FAIL = ''
        self.ENDC = ''

class MyDistributedStorageClient:

    socket.setdefaulttimeout(2)

    def __init__(self):
        self.a_client = xmlrpclib.ServerProxy("http://127.0.0.1:9595/")
        self.b_client = xmlrpclib.ServerProxy("http://127.0.0.1:9696/")
        self.c_client = xmlrpclib.ServerProxy("http://127.0.0.1:9797/")
        self.db_id = 1111

    def __str_to_bits(self, string):
        return binascii.b2a_hex(string)
    
    def __get_flows(self, string):
        global length
        hex_string = self.__str_to_bits(string)
        length = len(hex_string)

        a_flow = hex_string[0:length/2]
        b_flow = hex_string[length/2:]
        axorb_flow = hex(int(a_flow, 16) ^ int(b_flow, 16))[2:]
        if axorb_flow[-1] in '|L':
            axorb_flow = axorb_flow[:-1]
        return a_flow, b_flow, axorb_flow
    
    def __reconstruct(self, a=None, b=None, axorb=None):
        myList = [a, b, axorb]
        print myList.count(None)
        if myList.count(None) > 1:
            return "Unable To reconstruct the data: Two or more flows were not properly retrieved"
        if a and not b:
            b = hex(int(a, 16) ^ int(axorb, 16))[2:]
            if b[-1] in '|L': b = b[:-1]
        elif not a and b:
            a = hex(int(b, 16) ^ int(axorb, 16))[2:]
            if a[-1] in '|L': a = a[:-1]
        result = a + b
        print len(result)
        return binascii.a2b_hex(result)

    def ping(self):
        try:
            b_pong = self.b_client.ping()
            print mcolors.OKGREEN+"B_client OK"+mcolors.ENDC
        except:
            print mcolors.FAIL+"B_client is offline!"+mcolors.ENDC
        try:
            c_pong = self.c_client.ping()
            print mcolors.OKGREEN+"C_client OK"+mcolors.ENDC
        except:
            print mcolors.FAIL+"C_client is offline!"+mcolors.ENDC
        try:
            a_pong = self.a_client.ping()
            print mcolors.OKGREEN+"A_client OK"+mcolors.ENDC
        except:
            print mcolors.FAIL+"A_client is offline!"+mcolors.ENDC

    def read(self, db_id):
        try:
            a = self.a_client.read(db_id)
            print mcolors.OKGREEN+"A_client OK"+mcolors.ENDC
        except:
            print mcolors.FAIL+"A_client is offline!"+mcolors.ENDC
            a = None
        try:
            b = self.b_client.read(db_id)
            print mcolors.OKGREEN+"B_client OK"+mcolors.ENDC
        except:
            print mcolors.FAIL+"B_client is offline!"+mcolors.ENDC
            b = None
        try:
            c = self.c_client.read(db_id)
            print mcolors.OKGREEN+"C_client OK"+mcolors.ENDC
        except:
            print mcolors.FAIL+"C_client is offline!"+mcolors.ENDC
            c = None
        return self.__reconstruct(a, b, c)

    def write(self, data, db_id=None):
        a, b, c = self.__get_flows(data)
        if not db_id:
            db_id = self.db_id
        try:
            a = self.a_client.write(a, db_id)
            print mcolors.OKGREEN+"A_client OK"+mcolors.ENDC
        except:
            print mcolors.FAIL+"A_client is offline!"+mcolors.ENDC
        try:
            b = self.b_client.write(b, db_id)
            print mcolors.OKGREEN+"B_client OK"+mcolors.ENDC
        except:
            print mcolors.FAIL+"B_client is offline!"+mcolors.ENDC
        try:
            c = self.c_client.write(c, db_id)
            print mcolors.OKGREEN+"C_client OK"+mcolors.ENDC
        except:
            print mcolors.FAIL+"C_client is offline!"+mcolors.ENDC
        return a, b, c

global ping_result
client = MyDistributedStorageClient()
try:
    ping_result = client.ping()
except:
    print mcolors.FAIL+"clients offline!"+mcolors.ENDC
random_db_id = random.randrange(0, 1000)

if len(sys.argv) >= 2:
    try:
        file_contents = open(sys.argv[1], "r")
    except Exception as e:
        raise Exception("Could not open file. Details: %s" % str(e))
    file_read = file_contents.read()
    file_encoded = file_read.encode("utf16")
    # Encode and decode as necessary
    # Client only retrieves in the same format as stored
    write_result = client.write(file_encoded, random_db_id)
else:
    write_result = client.write("hello world!", random_db_id)
read_result = client.read(random_db_id)

print ping_result
print write_result
print read_result
