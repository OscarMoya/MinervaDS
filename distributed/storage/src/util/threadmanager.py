from threading import Thread
import traceback
class ThreadManager(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.setDaemon(True)

    @staticmethod
    def start_method_in_new_thread(method,params, **kwargs):
        thread = ThreadManager()
        thread.startMethod(method,params, **kwargs)
        return True

    def startMethod(self,method,params, **kwargs):
        if kwargs.get("name"):
            self.setName(kwargs.get("name"))
        self.__method = method
        self.__params = params
        self.start()

    def run(self):
        self.__method(*self.__params)
