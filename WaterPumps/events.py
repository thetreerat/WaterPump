# Author: Harold Clark
# Copyright Harold Clark 2017
#
try:
    import uasyncio.core as asyncio
except ImportError:
    import lib.uasyncio.core as asyncio

class Event():
    """Class for Events"""
    def __init__(self, lp=False,name='Name not defined',debug=False):
        """Inilized the Class Event"""
        self._name = name
        self.after = asyncio.sleep
        self.debug = debug
        self.clear()
        

    def name(self):
        return self._name

    
    def clear(self):
        """Clear the event if flag"""
        if self.debug:
            from utime import time
            print('''%s - %s: clearing event''' % (self._name, time()))
        self._flag = False
        self._data = None


    def __await__(self):
        """Method for making call wait"""
        while not self._flag:
            yield from self.after(0)


    __iter__ = __await__


    def is_set(self):
        """Method for returning the state of the event"""
        return self._flag


    def set(self, data=None):
        """Method for setting the event data, and flag"""
        self._flag = True
        self._data = data


    def value(self):
        """Method for return the Event data"""
        return self._data
