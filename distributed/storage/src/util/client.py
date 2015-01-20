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
        #print "HEX_STRING", hex_string

        """
        while True:
            length = len(hex_string)
            if not length % 4 == 0:
                hex_string = "0" + hex_string
            else:
                break
        """

        length = len(hex_string)

        a_flow = hex_string[0:length/2]
        b_flow = hex_string[length/2:]
        axorb_flow = hex(int(a_flow, 16) ^ int(b_flow, 16))[2:]
        if axorb_flow[-1] in '|L':
            axorb_flow = axorb_flow[:-1]

        """
        f = open("/home/i2cat/Documents/a_flow", "w+")
        f.write(a_flow)
        f.close()
        """

        #print "AFLOW", a_flow, len(a_flow)
        #print "BFLOW", b_flow, len(b_flow)
        #print "CFLOW", axorb_flow, len(axorb_flow)
        return a_flow, b_flow, axorb_flow
    
    def __reconstruct(self, a=None, b=None, axorb=None):
        print "-----Reconstructing:"
        #print "A", a, type(a)
        #print "B", b, type(b)
        #print "C", axorb, type(axorb)
        myList = [a, b, axorb]
        print myList.count(None)
        if myList.count(None) > 1:
            return "Unable To reconstruct the data: Two or more flows were not properly retrieved"
    
        if a and not b:
            print "bbbbbbb"
            b = hex(int(a, 16) ^ int(axorb, 16))[2:]
            if b[-1] in '|L': b = b[:-1]
            #print b
            #print a
            
        elif not a and b:
            print "aaaaaaa"
            a = hex(int(b, 16) ^ int(axorb, 16))[2:]
            if a[-1] in '|L': a = a[:-1]
            """
            f = open("/home/i2cat/Documents/axb_flow", "w+")
            f.write(a)
            f.close()
            #print "A: ", a
            """

        result = a + b
        #print "RESUTL", result, \
        print len(result)
        return binascii.a2b_hex(result)

    def ping(self):
        print "Ping round: "

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

        print "Read Round: "
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

        print "READING"
        #print a
        #print b
        #print c
        return self.__reconstruct(a, b, c)

    def write(self, data, db_id=None):
        a, b, c = self.__get_flows(data)
        if not db_id:
            db_id = self.db_id
        print "WRITE:"
        #print a, type(a)
        #print b, type(b)
        #print c, type(c)

        print "Write Round: "
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
#random_db_id = 222

if len(sys.argv) >= 2:
    try:
        file_contents = open(sys.argv[1], "r")
    except Exception as e:
        raise Exception("Could not open file. Details: %s" % str(e))

    file_read = file_contents.read()

    #file_encoded = binascii.b2a_hex(file_read)
    file_encoded = file_read.encode("utf16")

    # Encode and decode as necessary
    # Client only retrieves in the same format as stored
    write_result = client.write(file_encoded, random_db_id)

else:

    write_result = client.write("hello world!", random_db_id)
    #write_result = client.write("!&/*V+-=!?", random_db_id)

    """
    f = open("/home/i2cat/Downloads/Mi6.jpg", "r+")
    data = f.read()
    f.close()
    write_result = client.write(data, random_db_id)
    """
    """
    f = open("/home/i2cat/Documents/backup2.jpg", "w+")
    f.write(read_result)
    f.close()
    """
read_result = client.read(random_db_id)

print ping_result
print write_result
print read_result
