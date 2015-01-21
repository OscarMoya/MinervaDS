import binascii

class NF_Manager:

    def __init__(self):

        self.configure()
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
        #TODO: Check file_chunks contents to determine how to proceed on chunk_type assignation

        types = list()
        strings = list()

        for chunk in file_chunks():
            types.append(chunk['type'])
            strings.append(chunk['value'])

        return types, strings

    def deconstruct(self, full_file):

        global length
        file_chunks = list()


        hex_string = self.__str_to_bits(full_file)

        length = len(hex_string)

        a_flow = hex_string[0:length/2]
        b_flow = hex_string[length/2:]
        axorb_flow = hex(int(a_flow, 16) ^ int(b_flow, 16))[2:]

        if axorb_flow[-1] in '|L':
            axorb_flow = axorb_flow[:-1]

        file_chunks.append({"type": "A", "value": a_flow})
        file_chunks.append({"type": "B", "value": b_flow})
        file_chunks.append({"type": "AxB", "value": axorb_flow})

        return file_chunks


    def reconstruct(self, file_chunks):

        #TODO: Call chunk_parser to get the n-flows types, values
        types, values = self.chunk_parser(file_chunks)

        #TODO: For now, reconstruct just merges chunks' strings
        num_chunks = len(file_chunks)

        """
        if a and not b:
            b = hex(int(a, 16) ^ int(axorb, 16))[2:]
            if b[-1] in '|L':
                b = b[:-1]

        elif not a and b:
            a = hex(int(b, 16) ^ int(axorb, 16))[2:]
            if a[-1] in '|L':
                a = a[:-1]
        """
        result = ""

        for string in values:
            result += string

        self.__full_chunk = binascii.a2b_hex(result)
        return self.__full_chunk