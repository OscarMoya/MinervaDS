from distributed.storage.src.base.endpointnorth import EndPointNorthBase
from distributed.storage.lib.decorator.checkfailmode import checkfailmode

class MockedChannel(EndPointNorthBase):

    def __init__(self, fail_mode=False):
        self.fail_mode = False

    @checkfailmode
    def join(self, *args, **kwargs):
        return True

    @checkfailmode
    def leave(self, *args, **kwargs):
        return True

    @checkfailmode
    def read_request(self, *args, **kwargs):
        return True

    @checkfailmode
    def write_request(self, *args, **kwargs):
        return True

    @checkfailmode
    def initialize(self, *args, **kwargs):
        return True

