from threading import Thread

class ServiceThread(Thread):
    
    __method = None	
    __params = list()

    @staticmethod
    def start_in_new_thread(method,params):
    	thread = ServiceThread()	
    	thread.start_method(method,params)
    
    def start_method(self,method,params):
    	self.__method = method
        if not type(params) == list:
            params = [params]
    	self.__params = params
    	self.start()
    
    def run(self):	
    	self.__method(*self.__params)
