import binascii
import mmap
import os
import datetime
from distributed.storage.src.util.service_thread import ServiceThread


def get_time_now():
    return str(datetime.datetime.now().strftime('%M:%S.%f')[:-3])

def logger(message):
    ServiceThread.start_in_new_thread(logger_thread, message)

def logger_thread(message, log_file="/home/MinervaDS/time_nf_recons_v2.txt"):
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
        #TODO: Check file_chunks contents to determine how to oceed on chunk_type assignation

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
        #message = "Start - Time: %s " % (get_time_now())
        #logger(message)

        global length
        file_chunks = list()
        #print "full_file", full_file
        print "len(full_file)", len(full_file) 
        
        hex_string = self.__str_to_bits(full_file)        

        #print "len(hex_string)", len(hex_string)

        #try:
        #    mfd = os.open(full_file, os.O_RDONLY)
        #    filecontents = mmap.mmap(mfd, 0, prot=mmap.PROT_READ)
        #    file_size = filecontents.size()
        #    cont = filecontents.read(file_size)
        #except:
        #    cont = self.__str_to_bits(full_file)

        length = len(hex_string)
        #length = len(cont)  
        #length = len(full_file)

        temp_a = "/home/MinervaDS/a_flow_file"
        temp_b = "/home/MinervaDS/b_flow_file"
        temp_c = "/home/MinervaDS/c_flow_file"

        #a_flow = hex_string[0:length/2]
        a_flow_file = hex_string[0:(len(hex_string)/2)]
        print "a_flow size", len(a_flow_file)
        print "stripped len", len(a_flow_file.strip())
        self.store_temp(binascii.a2b_hex(a_flow_file), temp_a)
        #self.store_temp(a_flow_file, temp_a)
        del a_flow_file

        #b_flow = hex_string[length/2:]
        b_flow_file = hex_string[(len(hex_string)/2):]
        print "b_flow size", len(b_flow_file)
        self.store_temp(binascii.a2b_hex(b_flow_file), temp_b)
        #self.store_temp(b_flow_file, temp_b)
        del b_flow_file

        #axorb_flow = hex(int(a_flow, 16) ^ int(b_flow, 16))[2:]
        axorb_flow_file = hex(int(a_flow_file, 16) ^ int(b_flow_file, 16))[2:]
        print "c_flow size", len(axorb_flow_file)

        #a_flow = cont[0:length/2]
        #b_flow = cont[length/2:]
        #axorb_flow = hex(int(a_flow, 16) ^ int(b_flow, 16))[2:]
        #a_flow = full_file[0:length/2]
        #b_flow = full_file[length/2:]
        #axorb_flow = hex(int(a_flow, 16) ^ int(b_flow, 16))[2:]

        #if axorb_flow[-1] in '|L':
        #    axorb_flow = axorb_flow[:-1]

        if axorb_flow_file[-1] in '|L':
            axorb_flow_file = axorb_flow_file[:-1]

        #self.store_temp(axorb_flow_file, temp_c)
        self.store_temp(binascii.a2b_hex(axorb_flow_file), temp_c)
        del axorb_flow_file


        #file_chunks.append({"type": "A", "value": a_flow})
        #file_chunks.append({"type": "B", "value": b_flow})
        #file_chunks.append({"type": "AxB", "value": axorb_flow})

        file_chunks.append({"type": "A", "value": temp_a})
        file_chunks.append({"type": "B", "value": temp_b})
        file_chunks.append({"type": "AxB", "value": temp_c})

        print "file_chunks", file_chunks

        #message = "End - Time: %s " % (get_time_now())
        #logger(message) 
    
        return file_chunks


    def reconstruct(self, chunks):

        #message = "Start - Time: %s " % (get_time_now())
        #logger(message)

        #TODO: Call chunk_parser to get the n-flows types, values
        chunks = self.parse_chunks(chunks)

        #TODO: For now, reconstruct just merges chunks' strings
        #num_chunks = len(file_chunks)

        a = chunks.get(self.A_CHUNK_TYPE)
        b = chunks.get(self.B_CHUNK_TYPE)
        c = chunks.get(self.AxB_CHUNK_TYPE)

        if a and c and not b:
            b = hex(int(a, 16) ^ int(c, 16))[2:]
            if b[-1] in '|L':
                b = b[:-1]

        elif not a and b:
            a = hex(int(b, 16) ^ int(c, 16))[2:]
            if a[-1] in '|L':
                a = a[:-1]

        result = a + b

        self.__full_chunk = binascii.a2b_hex(result)
        
        #message = "End - Time: %s " % (get_time_now())
        #logger(message)

        return self.__full_chunk

    def parse_chunks(self, chunks):
        result = dict()
        for chunk in chunks:

            type = chunk.get(chunk.keys()[0]).get("chunk_type")
            data = chunk.get(chunk.keys()[0]).get("file_data")
            result[type] = data
        return result
