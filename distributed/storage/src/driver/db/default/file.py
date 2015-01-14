from distributed.storage.src.base.db import DBBase
import threading

try:
    import cPicle as pickle
except:
    import pickle


class FileDB(DBBase):

    def __init__(self):
        self.DB_NAME = "file_db"

    def save(self, **kwargs):
        #first, get the most updated data, just in case
        old_entry = self.filter(**kwargs)
        if not old_entry:
            data = self.load()
            data.append(kwargs)
            self.__write(data)
        else:
            #it should be just one coincidence, just need to update the entry
            self.update(old_entry, kwargs)

        return

    def load(self, **kwargs):
        if not kwargs:
            #load_all
            return self.__load_all()
        else:
            return self.filter(kwargs)

    def filter(self, **kwargs):
        matches = list()
        table = self.load_all()
        for entry in table:
            matched = False
            for field, value in kwargs:
                if not entry.get(field) == value:
                    break
            if matched:
                matches.append(entry)

        return matches

    def remove(self, entry):
        data = self.load()
        id = entry.get("id")
        i = 0 #I add manual counter, I don't trust possible hash matches done by list.index() on dicts
        for entry in data:
            if entry.get("id") == id:
                return i
                i += 1
        data.pop(i)

    def __load_all(self):
        with threading.Lock():
                f = open(self.DB_NAME, "a+")
                data = pickle.load(f)
                f.close()
        return data

    def __update(self, old_entry, new_entry):
         self.__remove(old_entry)
         self.save(new_entry)


    def __write(self, data):
        with threading.lock():
            f = file.open(self.DB_NAME, "wb")
            pickle.dump(data, f)
            f.close()


