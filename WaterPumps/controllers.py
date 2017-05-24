# Author: Harold Clark
# Copyright Harold Clark 2017
#

try:
    import lib.uasyncio as asyncio
except ImportError:
    import uasyncio as asyncio
try:
    import logging
except ImportError:
    import lib.logging as logging
    
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
        #s = socket.socket()
        print('''%s - %s: attemp to connect on port %s''' % (self.name(), time(), self.port))        
        reader, writer = yield from connectController(self.ip, self.port, True)
        if not reader:
            #self.notActiveEventset(time() + 10 + self.launchCount)
            self.launchEvent.set(time())
            self.controllerClose.set(time())
        else:
            print('''%s - %s: connected to %s on %s''' % (self.name(), time(), self.ip, self.port))
        while not self.controllerClose.is_set():
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
        #writer.awrite('exit\r\n')
        #s.close()
        self.notActiveEvent.set(time() + 10)
        
        
def connectController(ip, port, debug=False):
    if debug:
        print('''Controller at %s on port %s atempting connection ...'''% (ip,port))
    s = socket.socket()
    try:
        s.connect((ip,port))
    except OSError as e:
        print('''%s - %s: Error: %s''' % (ip, time(), e.args[0]))
        return None, e.args[0]
    if debug:
        print('''%s - %s: connection open''' % (ip, time()))
    yield IOWrite(s)
    if debug:
        print('''%s - %s: After IOWAIT''' % (ip, time()))
    return asyncio.StreamREader(s), asyncio.StreamWriter(s, {})