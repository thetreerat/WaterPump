# Author: Harold Clark
# Copyright Harold Clark 2017

try:
    import lib.uasyncio as asyncio
except ImportError:
    import uasyncio as asyncio
    
import socket
from utime import time

class remote(object):
    def __init__(self, name='Not Defined'):
        self._name = name
        self.MonitorList = []
    
    def name(self):
        return self._name
    
    def registerMonitor(self, monitorObject):
        self.MonitorList.append(monitorObject)           
        
    async def monitorRemote(self):
        main_loop = asyncio.get_event_loop()
        print('''Remote - %s: Monitor remote started.''' % (time()))
        while True:
            for M in self.MonitorList:
                if M.event.is_set():
                    main_loop.create_task(M.func(*M.args))
                    M.event.clear()
            await asyncio.sleep_ms(80)
        
        
    
