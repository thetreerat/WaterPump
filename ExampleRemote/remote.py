# Author: Harold Clark
# Copyright Harold Clark 2017
#
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
                M.event.is_set():
                    main_loop.create_task(m.func(*args))
            if parkPumpOn.is_set():
                self.pumpOn(parkPump, parkLed, parkPumpOn)
            if parkPumpOff.is_set():
                pumpOff(parkPump,parkLed,parkPumpOff)
            if lakePumpOn.is_set():
                pumpOn(lakePump,lakeLed, lakePumpOn)
            if lakePumpOff.is_set():
                pumpOff(lakePump,lakeLed,lakePumpOff)
            await asyncio.sleep_ms(80)
        
        
    
    def connectToPump(self, pumpIP, command, port=8888):
        s = socket.socket()
        try:
            s.connect((pumpIP, port))
        except OSError as e:
            if e.args[0] == 103:
                return 'no connection'
            else:
                raise
        s.send(command)
        pump_info = s.recv(512)
        s.send('exit\r\n')
        print('''%s - %s: %s''' % (pumpIP, time(), pump_info))
        return pump_info
