from distributed.storage.src.base.db import DBBase
import threading
import os
try:
    import cPickle as pickle
except:
    import pickle

class DefaultDB(DBBase):

    def __init__(self):
        self.DB_NAME = None
        self.PRIMARY_KEY = "id"

    def save(self, **kwargs):
        #first, get the most updated data, just in case
        data = self.load()
        id = kwargs.pop(self.PRIMARY_KEY)
        data[id] = kwargs

        self.__write(data)
        return True

    def load(self, **kwargs):
        if not kwargs:
            #load_all
            return self.__load_all()
        else:
            return self.filter(**kwargs)

    def filter(self, **kwargs):
        db = self.__load_all()
        id = kwargs.get(self.PRIMARY_KEY)
        if id:
            entry = db.get(id)
            kwargs.pop(self.PRIMARY_KEY)
            if not kwargs:
                return [{id:db[id]}]

            if set(kwargs.keys()).issubset(set(entry.keys())) and set(kwargs.values()).issubset(set(entry.values())):
                return [{id:db[id]}]
            else:
                return list()
        else:
            result = list()
            for id in db:
                entry = db[id]
                if set(kwargs.keys()).issubset(set(entry.keys())) and set(kwargs.values()).issubset(set(entry.values())):
                    result.append({id:db[id]})

            return result


    def remove(self, **kwargs):
        data = self.load()
        id = kwargs.get(self.PRIMARY_KEY)
        if not id:
            raise Exception("Missing ID")
        data.pop(id)
        self.__write(data)

    def __load_all(self):
        with threading.Lock():
            try:
                f = open(self.DB_NAME, "r+")
                data = pickle.load(f)
                f.close()
            except Exception as e:
                data = dict()
        return data

    def __write(self, data):
        with threading.Lock():
            f = open(self.DB_NAME, "wb")
            pickle.dump(data, f)
            f.close()