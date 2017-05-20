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
        namenc='''%s - no connection''' % (name)
        self.NoConnectionEvent = Event(namenc)
        nameoe='''%s - OSError''' % (name)
        self.OSErrorEvent = Event(nameoe)
    
    
    def name(self):
        return self._name
    
    
    def addMessage(command, event):
        self.messageQue.insert(0,(comaand,event))
    
        
    async def MonitorContoller(self, debug=False):
        s = socket.socket()
        print('''%s attemp to connect on port %s''' % (pumpIP, port))        
        try:
            s.connect((pumpIP, port))
        except OSError as e:
            if e.args[0] == 103:
                self.noConnectionEvent.set(time())
                return
            else:
                self.OSErrorEvent.set(e.args[0])
                return
        while True:
            await sleep_ms(500)
            if len(self.messageQue):
                 command, event = self.messageQue.pop()
                 s.send(command)
                 controllerMessage = s.recv(512).decode("utf-8")[:-2]
                 event.set(controllerMessage)
                 print('''%s - %s: return message: %s''' % (self.name(), time(),controllerMessage))
        s.send('exit\r\n')
        s.close()
        
