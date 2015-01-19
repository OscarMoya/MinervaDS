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

    def save(self, **kwargs):
        #first, get the most updated data, just in case
        data = self.load()
        id = kwargs.pop("id")
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
        matches = list()
        table = self.__load_all()

        for id in table:
            entry = table[id]
            id_match = None

            matched = False

            if kwargs.has_key("id"):
                id_match = False
                if not id == kwargs.pop("id"):
                    continue
                else:
                    id_match = True

            for field, value in kwargs:
                if not entry.get(field) == value:
                    matched = False
                    break
                matched = True

            if not kwargs and id_match in[True, False]:
                matched = id_match
            elif kwargs and id_match in[True, False]:
                matched = matched and id_match
            elif kwargs and not id_match in[True, False]:
                pass

            if matched:
                matches.append({id:entry})

        return matches

    def remove(self, **kwargs):
        data = self.load()
        id = kwargs.get("id")
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
            except:
                data = dict()
        return data

    def __write(self, data):
        with threading.Lock():
            f = open(self.DB_NAME, "wb")
            pickle.dump(data, f)
            f.close()