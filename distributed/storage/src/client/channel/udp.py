from distributed.storage.src.base.endpointnorth import ClientBase
import binascii
import os
import random
import sys
import xmlrpclib
import socket
import StringIO
import time

class mcolors:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.OKGREEN = ''
        self.FAIL = ''
        self.ENDC = ''

class UDPClient(ClientBase):
    stout = socket.setdefaulttimeout(5)
    sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __init__(self):
        self.__a_client = None
        self.__b_client = None
        self.__c_client = None
        self.__a_port = None
        self.__b_port = None
        self.__c_port = None
        self.__db_id = None
        self.__buf = 1016
        self.__message = "Hello world!"

    def __str_to_bits(self, string):
        return binascii.b2a_hex(string)

    def __get_flows(self, string):
        global length
        hex_string = self.__str_to_bits(string)
        
        length = len(hex_string)

        a_flow = hex_string[0:length / 2]
        b_flow = hex_string[length / 2:]
        axorb_flow = hex(int(a_flow, 16) ^ int(b_flow, 16))[2:]
        if axorb_flow[-1] in '|L': axorb_flow = axorb_flow[:-1]

        return a_flow, b_flow, axorb_flow

    def __reconstruct(self, a=None, b=None, axorb=None):
        print "-----Reconstructing:"
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
        # Fixed size of each field in bytes
        # f_proto = 1
        # f_action = 1
        # f_length = 2
        # f_db_id = 2
        # f_db_id = 2

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

    def __unpacker(self, data):
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
        print "Ping round... "

        action = "p"
        data_hex = hex(0)[2:]
        ln_data = len(data_hex)
        header = self.__headerize(action, ln_data, 0, 0)
        packet = header + data_hex

        try:
            self.sock1.connect((self.__a_client, self.__a_port))
            self.sock1.sendto(packet, (self.__a_client, self.__a_port))
            received = self.sock1.recv(4096)
            rcv, rcv_body = self.__unpacker(received)
            if rcv[1] == "P":
                print "Received: ", mcolors.OKGREEN + rcv[1] + " from SERVER A" + mcolors.ENDC
        except:
            print mcolors.FAIL + "SERVER A unknown" + mcolors.ENDC

        try:
            self.sock2.connect((self.__b_client, self.__b_port))
            self.sock2.sendto(packet, (self.__b_client, self.__b_port))
            received = self.sock2.recv(4096)
            rcv, rcv_body = self.__unpacker(received)
            if rcv[1] == "P":
                print "Received: ", mcolors.OKGREEN + rcv[1] + " from SERVER B" + mcolors.ENDC
        except:
            print mcolors.FAIL + "SERVER B unknown" + mcolors.ENDC

        try:
            self.sock3.connect((self.__c_client, self.__c_port))
            self.sock3.sendto(packet, (self.__c_client, self.__c_port))
            received = self.sock3.recv(4096)
            rcv, rcv_body = self.__unpacker(received)
            if rcv[1] == "P":
                print "Received: ", mcolors.OKGREEN + rcv[1] + " from SERVER AxB" + mcolors.ENDC
        except:
            print mcolors.FAIL + "SERVER AxB unknown" + mcolors.ENDC


    def read(self, db_id):
        print "Reading..."
        action = "r"
        sequences_ar = []
        sequences_br = []
        sequences_cr = []

        data_hex = hex(0)[2:]
        ln_data = len(data_hex)
        header = self.__headerize(action, ln_data, db_id, 0)
        packet = header + data_hex

        self.sock1.sendto(packet, (self.__a_client, self.__a_port))
        print mcolors.OKGREEN + "SERVER A request sent" + mcolors.ENDC
        a_input = StringIO.StringIO()
        try:
            r_a = self.sock1.recv(8192)

            while r_a:
                header, body = self.__unpacker(r_a)
                if header[1] == "R" and header[3] == db_id:
                    sequences_ar.append(header[4])
                    a_input.write(body)
                    r_a = self.sock1.recv(8192)
                else:
                    break

        except:
            print mcolors.FAIL + "Timeout" + mcolors.ENDC

        r_a = a_input.getvalue()
        if r_a != '':
            print "Received: ", mcolors.OKGREEN + "A" + mcolors.ENDC

        else:
            print mcolors.FAIL + "Wrong response" + mcolors.ENDC
            r_a = None

        a_input.close()

        self.sock2.sendto(packet, (self.__b_client, self.__b_port))
        print mcolors.OKGREEN + "SERVER B request sent" + mcolors.ENDC
        b_input = StringIO.StringIO()
        try:
            r_b = self.sock2.recv(8192)

            while r_b:
                header, body = self.__unpacker(r_b)
                if header[1] == "R" and header[3] == db_id:
                    sequences_br.append(header[4])
                    b_input.write(body)
                    r_b = self.sock2.recv(8192)
                else:
                    break

        except:
            print mcolors.FAIL + "Timeout" + mcolors.ENDC

        r_b = b_input.getvalue()

        if r_b != '':
            print "Received: ", mcolors.OKGREEN + "B" + mcolors.ENDC

        else:
            print mcolors.FAIL + "Wrong response" + mcolors.ENDC
            r_b = None
        b_input.close()

        self.sock3.sendto(packet, (self.__c_client, self.__c_port))
        print mcolors.OKGREEN + "SERVER AxB request sent" + mcolors.ENDC
        c_input = StringIO.StringIO()
        try:
            r_c = self.sock3.recv(8192)

            while r_c:
                header, body = self.__unpacker(r_c)
                if header[1] == "R" and header[3] == db_id:
                    sequences_cr.append(header[4])
                    c_input.write(body)
                    r_c = self.sock3.recv(8192)
                else:
                    break

        except:
            print mcolors.FAIL + "Timeout" + mcolors.ENDC

        r_c = c_input.getvalue()

        if r_c != '':
            print "Received: ", mcolors.OKGREEN + "AxB" + mcolors.ENDC

        else:
            print mcolors.FAIL + "Wrong response" + mcolors.ENDC
            r_c = None
        c_input.close()

        #print "SEQ_AR: ", sequences_ar
        #print "SEQ_BR: ", sequences_br
        #print "SEQ_CR: ", sequences_cr
        print "Lengths: ", len(sequences_ar), len(sequences_br), len(sequences_cr)
        return self.__reconstruct(r_a, r_b, r_c)


    def write(self, data, db_id=None):
        a, b, c = self.__get_flows(data)
        if not db_id:
            db_id = self.db_id
        print "Writing...:"
        action = "w"
        sequences_aw = []
        sequences_bw = []
        sequences_cw = []

        a_output = StringIO.StringIO(a)
        a_packet = a_output.read(1016)
        n_seq = 0
        try:
            while a_packet:
                sequences_aw.append(n_seq)
                ln_data = len(a_packet)
                header = self.__headerize(action, ln_data, db_id, n_seq)
                packet = header + a_packet
                self.sock1.sendto(packet, (self.__a_client, self.__a_port))
                time.sleep(0.00055)
                a_packet = a_output.read(1016)
                n_seq += 1
            
            print mcolors.OKGREEN + "Data sent to SERVER A" + mcolors.ENDC
            action = "D"
            header = self.__headerize(action, 0, db_id, 0)
            packet = header
            self.sock1.sendto(packet, (self.__a_client, self.__a_port))
            a_output.close()

        except socket.error as e:
            print e
            pass

        action = "w"
        b_output = StringIO.StringIO(b)
        #sock.connect((self.b_client, self.b_port))
        b_packet = b_output.read(1016)
        n_seq = 0

        try:
            while b_packet:
                sequences_bw.append(n_seq)
                ln_data = len(b_packet)
                header = self.__headerize(action, ln_data, db_id, n_seq)
                packet = header + b_packet
                self.sock2.sendto(packet, (self.__b_client, self.__b_port))
                time.sleep(0.00055)
                b_packet = b_output.read(1016)
                n_seq += 1

            print mcolors.OKGREEN + "Data sent to SERVER B" + mcolors.ENDC
            action = "D"
            header = self.__headerize(action, 0, db_id, 0)
            packet = header
            self.sock2.sendto(packet, (self.__b_client, self.__b_port))
            b_output.close()

        except socket.error as e:
            print e
            pass

        action = "w"
        c_output = StringIO.StringIO(c)
        #sock.connect((self.c_client, self.c_port))
        c_packet = c_output.read(1016)
        n_seq = 0
        try:
            while c_packet:
                sequences_cw.append(n_seq)
                ln_data = len(c_packet)
                header = self.__headerize(action, ln_data, db_id, n_seq)
                packet = header + c_packet
                self.sock3.sendto(packet, (self.__c_client, self.__c_port))
                time.sleep(0.00055)
                c_packet = c_output.read(1016)
                n_seq += 1

            print mcolors.OKGREEN + "Data sent to SERVER AxB" + mcolors.ENDC
            action = "D"
            header = self.__headerize(action, 0, db_id, 0)
            packet = header
            self.sock3.sendto(packet, (self.__c_client, self.__c_port))
            c_output.close()

        except socket.error as e:
            print e
            pass

        #print "SEQ_AW", sequences_aw
        #print "SEQ_BW", sequences_bw
        #print "SEQ_CW", sequences_cw
        print "Lengths: ", len(sequences_aw), len(sequences_bw), len(sequences_cw)
        self.sock1.close()
        self.sock2.close()
        self.sock3.close()
        return



#################################################################################
if __name__ == "__main__":

    client = UDPClient()
    client.ping()

    random_db_id = random.randrange(0, 1000)

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
        client.write(file_encoded, random_db_id)

    else:
        """
        #f = open("/home/i2cat/Downloads/sample.jpg", "r+")
        data = f.read()
        client.write(data, random_db_id)
        f.close()

        """
        client.message = "Goodbye, world..."
        client.write(client.message, random_db_id)
        
        time.sleep(4)


        read_result = client.read(random_db_id)
        """
        #f = open("/home/i2cat/Downloads/backup_sd.mp4", "w+")
        #f = open("/home/i2cat/Downloads/backup2.avi", "w+")
        f = open("/home/i2cat/Downloads/backup3.avi", "w+")
        #f = open("/home/i2cat/Downloads/backup.jpg", "w+")
        f.write(read_result)
        f.close()

        """
        print "read_result: ", read_result
        
        """
        read_result = client.read(random_db_id)
        print "read_result: ", read_result
        """
