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
        #print "len(full_file)", len(full_file) 
        
        #hex_string = self.__str_to_bits(full_file)        

        #print "len(hex_string)", len(hex_string)

        #try:
        #    mfd = os.open(full_file, os.O_RDONLY)
        #    filecontents = mmap.mmap(mfd, 0, prot=mmap.PROT_READ)
        #    file_size = filecontents.size()
        #    cont = filecontents.read(file_size)
        #except:
        #    cont = self.__str_to_bits(full_file)

        #length = len(hex_string)
        #length = len(cont)  
        #length = len(full_file)

        temp_a = "/home/MinervaDS/a_flow_file"
        temp_b = "/home/MinervaDS/b_flow_file"
        temp_c = "/home/MinervaDS/c_flow_file"

        #a_flow = hex_string[0:length/2]
        #a_flow_file = hex_string[0:(len(hex_string)/2)]
        a_flow_file = full_file[0:(len(full_file)/2)]
        print "a_flow size", len(a_flow_file)
        #self.store_temp(binascii.a2b_hex(a_flow_file), temp_a)
        self.store_temp(a_flow_file, temp_a)
        #del a_flow_file

        #b_flow = hex_string[length/2:]
        #b_flow_file = hex_string[(len(hex_string)/2):]
        b_flow_file = full_file[(len(full_file)/2):]
        print "b_flow size", len(b_flow_file)
        #self.store_temp(binascii.a2b_hex(b_flow_file), temp_b)
        self.store_temp(b_flow_file, temp_b)
        #del b_flow_file

        #axorb_flow = hex(int(a_flow, 16) ^ int(b_flow, 16))[2:]
        #axorb_flow_file = hex(int(a_flow_file, 16) ^ int(b_flow_file, 16))[2:]
        
        a_hex = binascii.hexlify(a_flow_file)
        
        b_hex = binascii.hexlify(b_flow_file)
        
        axorb_hex = hex(int(a_hex, 16) ^ int(b_hex, 16))[2:]
        #print "c_flow size", len(axorb_hex)
        
        del a_hex
        del b_hex

        #a_flow = cont[0:length/2]
        #b_flow = cont[length/2:]
        #axorb_flow = hex(int(a_flow, 16) ^ int(b_flow, 16))[2:]
        #a_flow = full_file[0:length/2]
        #b_flow = full_file[length/2:]
        #axorb_flow = hex(int(a_flow, 16) ^ int(b_flow, 16))[2:]

        #if axorb_flow[-1] in '|L':
        #    axorb_flow = axorb_flow[:-1]

        
        if axorb_hex[-1] in '|L':
            print str(axorb_hex[-20:])
            
            if (len(axorb_hex) % 2) != 0:
                axorb_hex = axorb_hex[:-1]        

            else:
                axorb_hex = "0" + axorb_hex[:-1]

        axorb_flow_file = binascii.unhexlify(axorb_hex)
        self.store_temp(axorb_flow_file, temp_c)
        print "c_flow size", len(axorb_flow_file)

        #self.store_temp(axorb_flow_file, temp_c)
        #self.store_temp(binascii.a2b_hex(axorb_flow_file), temp_c)
        del axorb_hex
        del a_flow_file
        del b_flow_file
        del axorb_flow_file


        #file_chunks.append({"type": "A", "value": a_flow})
        #file_chunks.append({"type": "B", "value": b_flow})
        #file_chunks.append({"type": "AxB", "value": axorb_flow})

        file_chunks.append({"type": "A", "value": temp_a})
        file_chunks.append({"type": "B", "value": temp_b})
        file_chunks.append({"type": "AxB", "value": temp_c})

        #print "file_chunks", file_chunks

        #message = "End - Time: %s " % (get_time_now())
        #logger(message) 
    
        return file_chunks


    def reconstruct(self, chunks):
        
        #global a_hex
        #global b_hex
        #global c_hex

        #message = "Start - Time: %s " % (get_time_now())
        #logger(message)

        #TODO: Call chunk_parser to get the n-flows types, values
        chunks = self.parse_chunks(chunks)

        #TODO: For now, reconstruct just merges chunks' strings
        #num_chunks = len(file_chunks)

        a = chunks.get(self.A_CHUNK_TYPE)
        b = chunks.get(self.B_CHUNK_TYPE)
        c = chunks.get(self.AxB_CHUNK_TYPE)
        """
        if a:
            print "chunk a", a, type(a), type(str(a))
        
        if b: 
            print "chunk b", b, type(b), type(str(b))

        if c: 
            print "chunk c", c, type(c), type(str(c))
        """

        if (a and c) and not b:
            print "A and C and not B"
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
            print "not A and B"
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
            print "A and B"
            
            a_str = str(a)
            b_str = str(b)
            a_hex = binascii.hexlify(a_str)
            b_hex = binascii.hexlify(b_str)
          
            del a_str
            del b_str
                   
        #print "len a_hex", len(a_hex)
        #print "len b_hex", len(b_hex)

        result = a_hex + b_hex

        #print "len hex result", len(result)

        self.__full_chunk = binascii.unhexlify(result)
        
        #print "len full_chunk", len(self.__full_chunk)
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
