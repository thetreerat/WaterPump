import uasyncio.core as asyncio
from WaterPumps.server_uasyncio import validCommand

class pump(object):
    def __init__(self, powerPin,startupTime=20, name='Pump'):
        """Init a pump"""
        import machine
        from WaterPumps.server_uasyncio import Event
        self.name = name
        self.Power = machine.Pin(powerPin,machine.Pin.OUT)
        self.startupTime = startupTime
        self.pumpClients = []
        self.pumpMonitorEvents = []
        self.currentRunData = False
        self.RunData = []
        self.pumpNotReadyEvent()  = Event() # event for pump to know it okay to start
        self.pumpStartEvent = Event() # event for services that need to do some in the startup period
        self.pumpFinishEvent = Event() # event for service that need to supply data 
        self.pumpRunningEvent = Event() # subscriber event for pumpOn
        self.pumpOnEvent = Event() # cleint event, pumpOn ie button, server, upstream server
        self.pumpOffEvent = Event() # client event, pumpOff ie button, server, downstream
        self.pumpOntimeEvent = Event() # client event, running time ie server
        self.registerMonitorEvent(self.pumpOnEvent, self.pumpOn)
        self.registerMonitorEvent(self.pumpOffEvent, self.pumpOff)
        self.registerMonitorEvent(self.pumpOnTimeEvent, self.onTime)
        self.registerMonitorEvent(self.pumpStatusEvent, self.pumpStatus)

        
        
    def pumpOn(self):
        """Turn on Pump if off. print and return action proformed"""
        from utime import time
        from WaterPump.pumpRunData import pumpRunData
        if not self.Power.value() and not self.pumpNotReadyEvent.is_set():
            self.currentRunData = pumpRunData()
            self.Power.value(True)
            self.pumpRunningEvent.set(self.currentRunDate.start)
            self.pumpFinishEvent.clear()
            self.pumpNotReadyEvent.clear()
            self.pumpStartEvent.set(self.currentRunData.start + self.startupTime)
            msg = """Pump Turned On"""
        elif self.Power.value():
            msg = """pump is already on!"""
        elif self.pumpNotReadyEvent.is_set() and not self.Power.value():
            msg = 'Pump not safe to start.'
        else:
            msg = 'pump in unknown state'
        print('''%s - %s: %s''' % (self.name,self.currentRunData.start,msg))
        return msg
    
    
    def pumpOff(self):
        """Turn off pump if on. prints action proformed and return action as string"""
        from utime import time
        print("""%s - %s: shuting down pump ...""" % (self.name, time()))        
        if self.Power.value():
            self.Power.value(False)
            self.currentRunData.finish(time())
            self.pumpFinishEvent.set(self.currentRunData.finsih)
            self.pumpOnEvent.clear()
            self.pumpStartEvent.clear()
            self.pumpNotReadyEvent.set(len(self.pumpClients))
            msg ="""Pump Turned off"""
        else:
            msg = """Pump was already off!"""
        print('''%s - %s: %s''' % (self.name, self.pumpFinishEvent.value(), msg))
        return msg
        
        
    def timeOn(self):
        import time
        if self.powerOnTime:
            TimeOn = str(time.time() - self.powerOnTime)
        else:
            TimeOn = 'Pump is Off'
        return TimeOn
    
    
    def pumpStatus(self):
        """check status of pump, and return test"""
        from WaterPumps.server_uasyncio import Event
        if self.Power.value():
            msg = """Pump is on, running time: %s""" % (self.timeOn())
        else:
            msg = """Pump is off."""

          
            
    def validCommandList(self):
        """return a list of valid server commands. if a fuction not to be exposed to server don't list"""
        list = []
        b = validCommand('pumpOn',self.pumpOnEvent)
        list.append(b)
        b = validCommand('pumpOff',self.pumpOffEvent)
        list.append(b)
        b = validCommand('pumpStatus',self.pumpStatusEvent)
        list.append(b)
        b = validCommand('timeOn',self.pumpTimeOnEvent) 
        list.append(b)
        return list
        
        
    def registerMonitorEvents(self, Event, func):
        self.pumpMonitorEvents.append((Event, func))
        
        
    def registerPumpClient(self, name):
        """register client to pump monitor and return valid Event handles"""
        self.pumpClient.append(name)
        return self.validCommandList()
    
    def regisgterPumpServer(self, name):
        self.pumpServer.append(name)
        e = []
        e.append(('pumpStartEvent', self.pumpStartEvent))
        e.append(('pumpRunningEvent', self.pumpRunningEvent))
        e.append(('pumpFinishEvent', self.pumpFinishEvent))
        e.append(('pumpNotReadyEvent'. self.pumpNotReadyEvent))
        return e
    
            
    async def pumpMonitor(self):
        """coroutine for handling pump requests"""
        while True:
            for event, func in self.monitorEvents():
                await asyncio.sleep_ms(50) 
                if event.is_set():
                    event.set(func())
                    event.clear()
           