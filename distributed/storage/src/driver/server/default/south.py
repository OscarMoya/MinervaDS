from distributed.storage.src.base.controllersouth import ControllerSouthBase
from distributed.storage.src.util.packetmanager import PacketManager

class ServerSouthDriver(ControllerSouthBase):

    def __init__(self, packet_manager=None, pipe=None):
        self.__packet_manager = packet_manager
        self.__pipe = pipe

    def ping(self):
        self.__alert_pipe(self.ping)
        return "PONG"

    def syn_request(self):
        result = self.__packet_manager.send_sync()
        self.__alert_pipe("syn_request")
        return result

    def set_packet_manager(self, manager):
        self.__packet_manager = manager

    def get_packet_manager(self):
        return self.__packet_manager

    def __alert_pipe(self, func, **kwargs):
        if self.__pipe:
            return self.__pipe.alert(func, **kwargs)