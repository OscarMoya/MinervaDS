from distributed.storage.src.driver.db.default.default import DefaultDB

class DefaultFileDB(DefaultDB):

    def __init__(self):
        DefaultDB.__init__(self)
        self.DB_NAME = "file"
        self.PRIMARY_KEY = "file_id"