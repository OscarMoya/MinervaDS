import random
from distributed.storage.src.driver.db.default.default import DefaultDB

class DefaultLocationDB(DefaultDB):

    def __init__(self, prefix=None):
        DefaultDB.__init__(self)
        self.DB_NAME = "location"
        self.PRIMARY_KEY = "chunk_id"
        if not prefix:
            prefix = str(random.randint(0,1000))
        self.DB_NAME= prefix+self.DB_NAME