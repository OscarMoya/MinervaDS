class processoutput(object):
    def __init__(self, func, *args, **kwargs):
        self.func = func

    def __get__(self, cls, *args, **kwargs):
        if cls:
            self.cls = cls
        return self

    def __call__(self, *args, **kwargs):
        def decorate(*args,**kwargs):
            def post_process( *args, **kwargs):
                result = self.func(self.cls,*args, **kwargs)
                if result == None:
                    result = True
                return result
            return post_process(*args, **kwargs)
        return decorate(*args, **kwargs)