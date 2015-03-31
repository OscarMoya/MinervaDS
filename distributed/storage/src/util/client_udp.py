import binascii
import os
import random
import sys
import socket
import StringIO
import time
import datetime
from service_thread import ServiceThread

def get_time_now(timeout=None):
    if timeout:
        t1 = datetime.datetime.now()
        t3 = t1 - datetime.timedelta(seconds=timeout)
        return str(t3.strftime('%M:%S.%f')[:-3])
    else:
        return str(datetime.datetime.now().strftime('%M:%S.%f')[:-3])

def logger(message):
    ServiceThread.start_in_new_thread(logger_thread, message)

def logger_thread(message, log_file="./TEST.txt"):
    if os.path.exists(log_file):
        l = open(log_file, 'a')
        l.write(message+"\n")

    else:
        l = open(log_file, 'wb')
        l.write(message+"\n")
    l.close()

class mcolors:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.OKGREEN = ''
        self.FAIL = ''
        self.ENDC = ''


class MyDistributedStorageClient:

    STOUT = socket.setdefaulttimeout(6)
    sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


    def __init__(self):
        self.a_client = "127.0.0.1"
        self.b_client = "127.0.0.1"
        self.c_client = "127.0.0.1"
        self.a_port = 9595
        self.b_port = 9696
        self.c_port = 9797
        self.db_id = 1111
        self.buf = 1016
        self.message = "Hello world!"

    def __str_to_bits(self, string):
        return binascii.b2a_hex(string)

    def __get_flows(self, string):
        global length
        hex_string = self.__str_to_bits(string)
        length = len(hex_string)

        a_flow = hex_string[0:length / 2]
        b_flow = hex_string[length / 2:]
        axorb_flow = hex(int(a_flow, 16) ^ int(b_flow, 16))[2:]
        if axorb_flow[-1] in '|L':
            axorb_flow = axorb_flow[:-1]
        return a_flow, b_flow, axorb_flow

    def __reconstruct(self, a=None, b=None, axorb=None):
        myList = [a, b, axorb]
        if myList.count(None) > 1:
            return "Unable To reconstruct the data: Two or more flows were not properly retrieved"
        if a and not b:
            b = hex(int(a, 16) ^ int(axorb, 16))[2:]
            if b[-1] in '|L': b = b[:-1]
        elif not a and b:
            a = hex(int(b, 16) ^ int(axorb, 16))[2:]
            if a[-1] in '|L': a = a[:-1]
        result = a + b
        return binascii.a2b_hex(result)

    def __headerize(self, action, length, db_id, seq):
        proto = self.__str_to_bits("u")
        act = self.__str_to_bits(action)
        ln = hex(length)[2:]
        db = hex(db_id)[2:]
        sq = hex(seq)[2:]
        # Padding: fill difference with chars "0", one byte each
        pd_ln = (4 - len(ln)) * "0" + ln
        pd_db = (4 - len(db)) * "0" + db
        pd_sq = (4 - len(sq)) * "0" + sq
        header = proto + act + pd_ln + pd_db + pd_sq
        return header

    def unpacker(self, data):
        header = []
        data_to_parse = StringIO.StringIO(data)
        header.append(binascii.a2b_hex(data_to_parse.read(2)))  # Protocol
        header.append(binascii.a2b_hex(data_to_parse.read(2)))  # Action
        header.append(int(data_to_parse.read(4), 16))  # Length
        header.append(int(data_to_parse.read(4), 16))  # DB_ID
        header.append(int(data_to_parse.read(4), 16))  # seq
        body = data_to_parse.read()
        return header, body

    def ping(self):
        action = "p"
        data_hex = hex(0)[2:]
        ln_data = len(data_hex)
        header = self.__headerize(action, ln_data, 0, 0)
        packet = header + data_hex
        try:
            self.sock1.connect((self.a_client, self.a_port))
            message = "Ping to: SERVER_A Time: %s" % get_time_now()     # LOGGER HERE
            logger(message)                                             # LOGGER HERE
            self.sock1.sendto(packet, (self.a_client, self.a_port))
            received = self.sock1.recv(4096)
            rcv, rcv_body = self.unpacker(received)
            if rcv[1] == "P":
                message = "Pong from: SERVER_A Time: %s" % get_time_now()   # LOGGER HERE
                logger(message)                                             # LOGGER HERE
        except:
            print mcolors.FAIL + "A Server unknown" + mcolors.ENDC
        try:
            self.sock2.connect((self.b_client, self.b_port))
            message = "Ping to: SERVER_B Time: %s" % get_time_now()     # LOGGER HERE
            logger(message)                                             # LOGGER HERE
            self.sock2.sendto(packet, (self.b_client, self.b_port))
            received = self.sock2.recv(4096)
            rcv, rcv_body = self.unpacker(received)
            if rcv[1] == "P":
                message = "Pong from: SERVER_B Time: %s" % get_time_now()   # LOGGER HERE
                logger(message)                                             # LOGGER HERE
        except:
            print mcolors.FAIL + "B Server unknown" + mcolors.ENDC
        try:
            self.sock3.connect((self.c_client, self.c_port))
            message = "Ping to: SERVER_AxB Time: %s" % get_time_now()       # LOGGER HERE
            logger(message)                                                 # LOGGER HERE
            self.sock3.sendto(packet, (self.c_client, self.c_port))
            received = self.sock3.recv(4096)
            rcv, rcv_body = self.unpacker(received)
            if rcv[1] == "P":
                message = "Pong from: SERVER_AxB Time: %s" % get_time_now()     # LOGGER HERE
                logger(message)                                                 # LOGGER HERE
        except:
            print mcolors.FAIL + "C Server unknown" + mcolors.ENDC

    def read(self, db_id):
        action = "r"
        sequences_ar = []
        sequences_br = []
        sequences_cr = []
        data_hex = hex(0)[2:]
        ln_data = len(data_hex)
        header = self.__headerize(action, ln_data, db_id, 0)
        packet = header + data_hex
        message = "Read start at: SERVER_A Time: %s" % get_time_now()       # LOGGER HERE
        logger(message)                                                     # LOGGER HERE
        self.sock1.sendto(packet, (self.a_client, self.a_port))
        print mcolors.OKGREEN + "Request A sent" + mcolors.ENDC
        a_input = StringIO.StringIO()
        try:
            r_a = self.sock1.recv(8192)
            while r_a:
                header, body = self.unpacker(r_a)
                if header[1] == "R" and header[3] == db_id:
                    sequences_ar.append(header[4])
                    a_input.write(body)
                    r_a = self.sock1.recv(8192)
                else:
                    break
        except:
            print mcolors.FAIL + "TIMEOUT!" + mcolors.ENDC

        r_a = a_input.getvalue()
        if r_a != '':
            message = "Read end at: SERVER_A Time: %s" % get_time_now(timeout=2)    # LOGGER HERE
            logger(message)                                                         # LOGGER HERE
            print "Received: ", mcolors.OKGREEN + "A" + mcolors.ENDC
        else:
            print mcolors.FAIL + "WRONG response" + mcolors.ENDC
            r_a = None
        a_input.close()

        message = "Read start at: SERVER_B Time: %s" % get_time_now()               # LOGGER HERE
        logger(message)                                                             # LOGGER HERE
        self.sock2.sendto(packet, (self.b_client, self.b_port))
        print mcolors.OKGREEN + "Request B sent" + mcolors.ENDC
        b_input = StringIO.StringIO()
        try:
            r_b = self.sock2.recv(8192)
            while r_b:
                header, body = self.unpacker(r_b)
                if header[1] == "R" and header[3] == db_id:
                    sequences_br.append(header[4])
                    b_input.write(body)
                    r_b = self.sock2.recv(8192)
                else:
                    break

        except:
            print mcolors.FAIL + "TIMEOUT!" + mcolors.ENDC

        r_b = b_input.getvalue()
        if r_b != '':
            message = "Read end at: SERVER_B Time: %s" % get_time_now(timeout=2)    # LOGGER HERE
            logger(message)                                                         # LOGGER HERE
            print "Received: ", mcolors.OKGREEN + "B" + mcolors.ENDC
        else:
            print mcolors.FAIL + "WRONG response" + mcolors.ENDC
            r_b = None
        b_input.close()

        message = "Read start at: SERVER_AxB Time: %s" % get_time_now()     # LOGGER HERE
        logger(message)                                                     # LOGGER HERE
        self.sock3.sendto(packet, (self.c_client, self.c_port))
        print mcolors.OKGREEN + "Request AxB sent" + mcolors.ENDC
        c_input = StringIO.StringIO()
        try:
            r_c = self.sock3.recv(8192)
            while r_c:
                header, body = self.unpacker(r_c)
                if header[1] == "R" and header[3] == db_id:
                    sequences_cr.append(header[4])
                    c_input.write(body)
                    r_c = self.sock3.recv(8192)
                else:
                    break

        except:
            print mcolors.FAIL + "TIMEOUT!" + mcolors.ENDC

        r_c = c_input.getvalue()
        if r_c != '':
            message = "Read end at: SERVER_AxB Time: %s" % get_time_now(timeout=2)  # LOGGER HERE
            logger(message)                                                         # LOGGER HERE
            print "Received: ", mcolors.OKGREEN + "AxB" + mcolors.ENDC

        else:
            print mcolors.FAIL + "WRONG response" + mcolors.ENDC
            r_c = None
        c_input.close()
        return self.__reconstruct(r_a, r_b, r_c)


    def write(self, data, db_id=None):
        a, b, c = self.__get_flows(data)
        if not db_id:
            db_id = self.db_id
        action = "w"
        sequences_aw = []
        sequences_bw = []
        sequences_cw = []

        message = "Write start to: SERVER_A Time: %s" % get_time_now()      # LOGGER HERE
        logger(message)                                                     # LOGGER HERE
        a_output = StringIO.StringIO(a)
        a_packet = a_output.read(1024)
        n_seq = 0
        try:
            while a_packet:
                sequences_aw.append(n_seq)
                ln_data = len(a_packet)
                header = self.__headerize(action, ln_data, db_id, n_seq)
                packet = header + a_packet
                self.sock1.sendto(packet, (self.a_client, self.a_port))
                time.sleep(0.0002)
                a_packet = a_output.read(1024)
                n_seq += 1
            print mcolors.OKGREEN + "A sent" + mcolors.ENDC
            action = "D"
            header = self.__headerize(action, 0, db_id, 0)
            packet = header
            self.sock1.sendto(packet, (self.a_client, self.a_port))
            message = "Write end to: SERVER_A Time: %s" % get_time_now()    # LOGGER HERE
            logger(message)                                                 # LOGGER HERE
            a_output.close()
        except socket.error as e:
            print mcolors.FAIL+"SERVER A: "+str(e)+mcolors.ENDC
            pass

        action = "w"
        message = "Write start to: SERVER_B Time: %s" % get_time_now()      # LOGGER HERE
        logger(message)                                                     # LOGGER HERE
        b_output = StringIO.StringIO(b)
        b_packet = b_output.read(1024)
        n_seq = 0

        try:
            while b_packet:
                sequences_bw.append(n_seq)
                ln_data = len(b_packet)
                header = self.__headerize(action, ln_data, db_id, n_seq)
                packet = header + b_packet
                self.sock2.sendto(packet, (self.b_client, self.b_port))
                time.sleep(0.00012)
                b_packet = b_output.read(1024)
                n_seq += 1
            print mcolors.OKGREEN + "B sent" + mcolors.ENDC
            action = "D"
            header = self.__headerize(action, 0, db_id, 0)
            packet = header
            self.sock2.sendto(packet, (self.b_client, self.b_port))
            message = "Write end to: SERVER_B Time: %s" % get_time_now()    # LOGGER HERE
            logger(message)                                                 # LOGGER HERE
            b_output.close()

        except socket.error as e:
            print mcolors.FAIL+"SERVER B: "+str(e)+mcolors.ENDC
            pass

        action = "w"
        message = "Write start to: SERVER_AxB Time: %s" % get_time_now()    # LOGGER HERE
        logger(message)                                                     # LOGGER HERE
        c_output = StringIO.StringIO(c)
        c_packet = c_output.read(1024)
        n_seq = 0
        try:
            while c_packet:
                sequences_cw.append(n_seq)
                ln_data = len(c_packet)
                header = self.__headerize(action, ln_data, db_id, n_seq)
                packet = header + c_packet
                self.sock3.sendto(packet, (self.c_client, self.c_port))
                time.sleep(0.00012)
                c_packet = c_output.read(1024)
                n_seq += 1
            print mcolors.OKGREEN + "AxB sent" + mcolors.ENDC
            action = "D"
            header = self.__headerize(action, 0, db_id, 0)
            packet = header
            self.sock3.sendto(packet, (self.c_client, self.c_port))
            message = "Write end to: SERVER_AxB Time: %s" % get_time_now()  # LOGGER HERE
            logger(message)                                                 # LOGGER HERE
            c_output.close()

        except socket.error as e:
            print mcolors.FAIL+"SERVER AxB: "+str(e)+mcolors.ENDC
            pass
        print "LENGTHS: ", len(sequences_aw), len(sequences_bw), len(sequences_cw)
        return

client = MyDistributedStorageClient()

client.ping()

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
    client.write(file_encoded, random_db_id)

else:
    f = open("/home/i2cat/Downloads/trailer_sd.mp4", "r+")
    data = f.read()
    client.write(data, random_db_id)
    f.close()
    time.sleep(4)
    read_result = client.read(random_db_id)

    f = open("/home/i2cat/Downloads/backup_sd.mp4", "w+")
    f.write(read_result)
    f.close()

client.sock1.close()
client.sock2.close()
client.sock3.close()
