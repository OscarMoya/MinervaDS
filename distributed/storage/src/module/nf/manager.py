import binascii
import sys


class NF_Manager:

    def __init__(self):

        self.__a_chunk = None
        self.__b_chunk = None
        self.__c_chunk = None

        self.__full_chunk = None

    def __str_to_bits(self, string):
        return binascii.b2a_hex(string)

    def chunk_parser(self, file_chunks):
        #TODO: Check file_chunks contents to determine how to proceed on chunk_type assignation

        num_chunks = file_chunks.count(None)

        """
        for num in xrange(num_chunks):
            pass
        """

        for chunk in file_chunks:
            if chunk['type'] == "CHUNK_A_TYPE":
                self.__a_chunk = chunk.get('value')
            elif chunk['type'] == "CHUNK_B_TYPE":
                self.__b_chunk = chunk.get('value')
            else:       #chunk.type == "CHUNK_AXB_TYPE"
                self.__c_chunk = chunk.get('value')

        return self.__a_chunk, self.__b_chunk, self.__c_chunk

    def deconstruct(self, full_file):
        global length

        file_data = full_file.read()

        hex_string = self.__str_to_bits(file_data)

        length = len(hex_string)

        a_flow = hex_string[0:length/2]
        b_flow = hex_string[length/2:]
        axorb_flow = hex(int(a_flow, 16) ^ int(b_flow, 16))[2:]
        if axorb_flow[-1] in '|L':
            axorb_flow = axorb_flow[:-1]


        return a_flow, b_flow, axorb_flow


    def reconstruct(self, file_chunks):

        #TODO: Call chunk_parser to get the tri-flows
        a, b, axorb = self.chunk_parser(file_chunks)

        """
        a = None
        b = None
        axorb = None
        """

        myList = [a, b, axorb]
        print myList.count(None)

        if myList.count(None) > 1:
            print ("Unable To reconstruct the data: Two or more flows were not properly retrieved")
            return

        if a and not b:
            b = hex(int(a, 16) ^ int(axorb, 16))[2:]
            if b[-1] in '|L':
                b = b[:-1]

        elif not a and b:
            a = hex(int(b, 16) ^ int(axorb, 16))[2:]
            if a[-1] in '|L':
                a = a[:-1]

        result = a + b
        return binascii.a2b_hex(result)