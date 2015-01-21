class checkfailmode(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, cls, cls_type):
        def decorate(*args,**kwargs):
            if cls.fail_mode:
                 raise Exception ("Error on function %s with args %s" %(self.func.__name__, str(kwargs)))
            return self.func(cls, *args,**kwargs)
        return decorate
