from distributed.storage.lib.decorator.checkfailmode import checkfailmode

class MockedPacketManager:

    def __init__(self, fail_mode=False):
        self.fail_mode = fail_mode

    @checkfailmode
    def send_sync(self, *args, **kwargs):
        return True