from threading import Thread

class ThreadManager(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.setDaemon(True)

    @staticmethod
    def start_method_in_new_thread(method,params):
        thread = ThreadManager()
        thread.startMethod(method,params)

    def startMethod(self,method,params):
        self.__method = method
        self.__params = params
        self.start()

    def run(self):
        self.__method(*self.__params)