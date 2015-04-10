import binascii
import mmap
import os
import datetime
from distributed.storage.src.util.service_thread import ServiceThread


def get_time_now():
    return str(datetime.datetime.now().strftime('%M:%S.%f')[:-3])

def logger(message):
    ServiceThread.start_in_new_thread(logger_thread, message)

def logger_thread(message, log_file="/home/MinervaDS/time_nf_recons_v5.txt"):
    if os.path.exists(log_file):
        l = open(log_file, 'a')
        l.write(message+"\n")

    else:
        l = open(log_file, 'wb')
        l.write(message+"\n")
    l.close()

class NFManager:

    def __init__(self):

        self.configure()
        self.A_CHUNK_TYPE = "A"
        self.B_CHUNK_TYPE = "B"
        self.AxB_CHUNK_TYPE = "AxB"
        self.__full_chunk = None

    def configure(self):
        pass

    def __str_to_bits(self, string):
        return binascii.b2a_hex(string)

    def chunk_parser(self, file_chunks):
        """
        file_chunks = list<chunk>()
        chunk = {"type": "type",
                "value": "string"}
        """
        # TODO: Check file_chunks contents to determine how to oceed on chunk_type assignation
        types = list()
        strings = list()

        for chunk in file_chunks():
            types.append(chunk['type'])
            strings.append(chunk['value'])

        return types, strings

    def store_temp(self, chunk, temp_file):
        if os.path.exists(temp_file):
            l = open(temp_file, 'w')
            l.write(chunk)

        else:
            l = open(temp_file, 'w')
            l.write(chunk)
        l.close()

    def remove_temp(self, chunk, temp_file):
        if os.path.exists(temp_file):
            pass

    def deconstruct(self, full_file):
        global length
        file_chunks = list()

        temp_a = "/home/MinervaDS/a_flow_file"
        temp_b = "/home/MinervaDS/b_flow_file"
        temp_c = "/home/MinervaDS/c_flow_file"

        a_flow_file = full_file[0:(len(full_file)/2)]
        self.store_temp(a_flow_file, temp_a)

        b_flow_file = full_file[(len(full_file)/2):]
        self.store_temp(b_flow_file, temp_b)
        
        a_hex = binascii.hexlify(a_flow_file)
        b_hex = binascii.hexlify(b_flow_file)
        axorb_hex = hex(int(a_hex, 16) ^ int(b_hex, 16))[2:]
        
        del a_hex
        del b_hex
      
        #if axorb_hex[-1] in '|L':          
        if True:   
            if (len(axorb_hex) % 2) != 0:
                axorb_hex = axorb_hex[:-1]
            else:
                axorb_hex = "0" + axorb_hex[:-1]
        
        axorb_flow_file = binascii.unhexlify(axorb_hex)
        self.store_temp(axorb_flow_file, temp_c)

        del axorb_hex
        del a_flow_file
        del b_flow_file
        del axorb_flow_file

        file_chunks.append({"type": "A", "value": temp_a})
        file_chunks.append({"type": "B", "value": temp_b})
        file_chunks.append({"type": "AxB", "value": temp_c})

        return file_chunks

    def reconstruct(self, chunks):
        # TODO: Call chunk_parser to get the n-flows types, values
        chunks = self.parse_chunks(chunks)

        # TODO: For now, reconstruct just merges chunks' strings
        a = chunks.get(self.A_CHUNK_TYPE)
        b = chunks.get(self.B_CHUNK_TYPE)
        c = chunks.get(self.AxB_CHUNK_TYPE)

        if (a and c) and not b:
            a_str = str(a)
            c_str = str(c)
            del a
            del c
            a_hex = binascii.hexlify(a_str) 
            c_hex = binascii.hexlify(c_str)
            b_hex = hex(int(a_hex, 16) ^ int(c_hex, 16))[2:]
            if b_hex[-1] in '|L':
                b_hex = b_hex[:-1]
            del a_str
            del c_str
        elif not a and b:
            b_str = str(b)
            c_str = str(c)
            del b
            del c
            b_hex = binascii.hexlify(b_str)
            c_hex = binascii.hexlify(c_str)
            a_hex = hex(int(b_hex, 16) ^ int(c_hex, 16))[2:]
            if a_hex[-1] in '|L':
                a_hex = a_hex[:-1]
            del b_str
            del c_str
        elif a and b:           
            a_str = str(a)
            b_str = str(b)
            a_hex = binascii.hexlify(a_str)
            b_hex = binascii.hexlify(b_str)
            del a_str
            del b_str
        result = a_hex + b_hex
        
        if (len(result) % 2) != 0:
                
                print "Odd-lenght"
                print len(result)
                print result
                #result = "0" + result
      
        self.__full_chunk = binascii.unhexlify(result)
        return self.__full_chunk

    def parse_chunks(self, chunks):
        result = dict()
        for chunk in chunks:
            type = chunk.get(chunk.keys()[0]).get("chunk_type")
            data = chunk.get(chunk.keys()[0]).get("file_data")
            result[type] = data
        return result
