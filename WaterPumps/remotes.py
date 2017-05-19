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
            #if parkPumpOn.is_set():
            #    self.pumpOn(parkPump, parkLed, parkPumpOn)
            #if parkPumpOff.is_set():
            #    pumpOff(parkPump,parkLed,parkPumpOff)
            #if lakePumpOn.is_set():
            #    pumpOn(lakePump,lakeLed, lakePumpOn)
            #if lakePumpOff.is_set():
            #    pumpOff(lakePump,lakeLed,lakePumpOff)
            await asyncio.sleep_ms(80)
        
        
    
def connectToPump(pumpIP, command, port=8888):
    s = socket.socket()
    print('''%s attemp to connect on port %s''' % (pumpIP, port))
    try:
        s.connect((pumpIP, port))
    except OSError as e:
        if e.args[0] == 103:
            return 'no connection'
        elif e.args[0] == 104:
            return 'connection reset'
        else:
            raise
        
    s.send(command)
    pump_info = s.recv(512).decode("utf-8")
    s.send('exit\r\n')
    print('''%s - %s: %s''' % (pumpIP, time(), pump_info))
    return pump_info
