from distributed.storage.src.base.endpointnorth import EndPointNorthBase
from distributed.storage.lib.decorator.checkfailmode import checkfailmode

class MockedChannel(EndPointNorthBase):

    def __init__(self, fail_mode=False, pipe=None):
        self.pipe = pipe
        self.fail_mode = False

    @checkfailmode
    def join(self, *args, **kwargs):

        print "Called Join!!!!!"
        self.alert(self.join)
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

    def alert(self,func, *args, **kwargs):
        print "on alert"
        print self.pipe
        if self.pipe:
             self.pipe.alert("Method triggered %s" %func.__name__)

