# Author: Harold Clark
# Copyright Harold Clark 2017
#
import uasyncio.core as asyncio
class Event():
    """Class for Events"""
    def __init__(self, lp=False, eventType=1):
        """Inilized the Class Event"""
        self.after = asyncio.sleep
        self._eventType = eventType
        self.clear()
        
        
    def clear(self):
        """Clear the event if flag is 1 or type=1"""
        if self._eventType==2 and self._flag>1:
            self._flag -= 1    
        else:
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
        if self._eventType==2:
            self._flag=data
        else:
            self._flag = True
        self._data = data


    def value(self):
        """Method for return the Event data"""
        return self._data
