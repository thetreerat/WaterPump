# Author: Harold Clark
# Copyright Harold Clark 2017
#

try:
    import lib.uasyncio as asyncio
except ImportError:
    import uasyncio as asyncio
from utime import time
import socket
from WaterPumps.events import Event

class controller(object):
    def __init__(self, ip, name='Not Defined', port=8888):
        self.ip = ip
        self._name = name
        self.port = port
        self.validComandList = []
        self.messageQue = []
        self.noConnectionEvent = Event(name='''%s - no connection''' % (name))
        self.OSErrorEvent = Event(name='''%s - OSError''' % (name))
        self.notActiveEvent = Event(name='''%s - Not Active''' % (name))
        self.notActiveEvent.set(time() + 5)
        self.launchEvent = Event(name='''%s - Lauch Event''' % (name))
        self.launchEvent.set(time())
        self.launchCount = 0
        self.controllerClose = Event()
    
    def name(self):
        return self._name
    
    
    def addMessage(command, event):
        self.messageQue.insert(0,(comaand,event))
    
        
    async def monitorController(self, debug=False):
        s = socket.socket()
        print('''%s attemp to connect on port %s''' % (self.name(), self.port))        
        reader, writer = yield from asyncio.open_connection(self.ip, self.port)
        print('''%s - %s: connected to %s on %s''' % (self.name(), time(), self.ip, self.port))
        while not self.controllerCloseEvent.is_set():
            await asyncio.sleep_ms(500)
            if len(self.messageQue):
                command, event = self.messageQue.pop()
                yield from writer.awrite(command) 
                controllerMessage = yield from reader.read()
                controllerMessage = controllerMessage.decode("utf-8")[:-2]
                #cleanMessage = controllerMessage
                event.set(controllerMessage)
                if debug:
                    print('''%s - %s: return message: %s''' % (self.name(), time(),controllerMessage))
        writer.awrite('exit\r\n')
        s.close()
        self.notActiveEvent.set(time() + 10)