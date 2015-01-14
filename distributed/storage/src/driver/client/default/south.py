from distributed.storage.src.base.controllersouth import ControllerSouthBase
from distributed.storage.src.util.packetmanager import PacketManager

class ClientSouthDriver(ControllerSouthBase):

    def __init__(self):
        pass

    def ping(self):
        return "PONG"

    def syn_request(self):
        result = PacketManager.send_sync()
        return result


