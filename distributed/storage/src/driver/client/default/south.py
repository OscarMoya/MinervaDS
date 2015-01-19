from distributed.storage.src.base.controllersouth import ControllerSouthBase
from distributed.storage.src.util.packetmanager import PacketManager

class ClientSouthDriver(ControllerSouthBase):

    def __init__(self, packet_manager=None):
        self.__packet_manager = packet_manager

    def ping(self):
        return "PONG"

    def syn_request(self):
        result = self.__packet_manager.send_sync()
        return result

    def set_packet_manager(self, manager):
        self.__packet_manager = manager

    def get_packet_manager(self):
        return self.__packet_manager


