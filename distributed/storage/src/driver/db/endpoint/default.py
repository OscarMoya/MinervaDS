from distributed.storage.src.driver.db.default.default import DefaultDB

class DefaultEndPointDB(DefaultDB):

    def __init__(self):
        DefaultDB.__init__(self)
        self.DB_NAME = "endpoint"