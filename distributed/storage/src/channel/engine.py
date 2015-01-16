import os
import re
import types

class ChannelEngine:

    def __init__(self):
        pass

    def __get_python_file(self, cType):
        #TODO: get_python_file(channel_type)
        raise NotImplementedError

    def load_type(self, channel_type):
        channel_module = None
        model_dir = os.path.dirname(__file__) + "/types/" #ChannelTypes Location Location; removed ".." from dir path
        for filename in os.listdir(model_dir):
            if filename == self.__get_python_file(channel_type):
                # Import the model file and find all clases inside it.
                channel_module = __import__(channel_type)
                break
        if channel_module:
            return channel_module.launch()
        else:
            raise Exception("Channel Type Not Found")




