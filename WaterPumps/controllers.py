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
    
    
    def name(self):
        return self._name
    
    
    def addMessage(command, event):
        self.messageQue.insert(0,(comaand,event))
    
        
    async def monitorController(self, debug=False):
        s = socket.socket()
        print('''%s attemp to connect on port %s''' % (self.name(), self.port))        
        try:
            s.connect((self.ip, self.port))
        except OSError as e:
            if e.args[0] == 103:
                self.noConnectionEvent.set(time())
                print('''%s - %s: no connection to %s on port %s''' % (self.name(), time(), self.ip, self.port))
                self.launchEvent.set()
                self.notActiveEvent.set(time() + 10)
                return
            else:
                self.OSErrorEvent.set(e.args[0])
                raise
        print('''%s - %s: connected to %s on %s''' % (self.name(), time(), self.ip, self.port))
        while True:
            await asyncio.sleep_ms(500)
            if len(self.messageQue):
                 command, event = self.messageQue.pop()
                 try:
                    s.send(command)
                 except OSError as e:
                    print(e)
                    s.close()
                    self.activeEvent.clear()
                    raise
                 controllerMessage = s.recv(512).decode("utf-8")[:-2]
                 event.set(controllerMessage)
                 if debug:
                    print('''%s - %s: return message: %s''' % (self.name(), time(),controllerMessage))
        s.send('exit\r\n')
        s.close()
        self.notActiveEvent.set(time() + 10)
        
