import functools

from PyQt5.QtCore import QObject


def singleton (cls) :
    cls._instance = None
    cls._initialized = False
    
    @functools.wraps(cls.__new__)
    def new (cls, *args, **kwargs) :
        if cls._instance is None :
            try :
                cls._instance = object.__new__(cls)
            except :
                cls._instance = QObject.__new__(cls)
        return cls._instance

    old_init = cls.__init__

    @functools.wraps(cls.__init__)
    def init (self, *args, **kwargs) :
        if not cls._initialized :
            old_init(self, *args, **kwargs)
            cls._initialized = True

    cls.__new__ = new
    cls.__init__ = init

    return cls
