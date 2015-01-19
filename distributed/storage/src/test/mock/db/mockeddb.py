from distributed.storage.src.base.db import DBBase
from distributed.storage.lib.decorator.checkfailmode import checkfailmode

class MockedDB(DBBase):

    def __init__(self, fail_mode=False):
        self.value = {}
        self.random_entry = {777:{"a":"a", "b":"b"}}
        self.fail_mode = fail_mode

    @checkfailmode
    def save(self, **kwargs):
        self.value = self.random_entry
        return self.value

    @checkfailmode
    def load(self, **kwargs):
        return self.value

    @checkfailmode
    def filter(self, **kwargs):
        if kwargs.get("chunk_type") == "A":
            return [{"server_url":"URL_A"}]
        elif kwargs.get("chunk_type") == "B":
            return [{"server_url":"URL_B"}]
        elif kwargs.get("chunk_type") == "AxB":
            return [{"server_url":"URL_AxB"}]
        else:
            return [{"server_url":"URL_A"}, {"server_url":"URL_B"}, {"server_url":"URL_AxB"}]

    @checkfailmode
    def remove(self, entry):
        self.value = {}
