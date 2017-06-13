# Author: Harold Clark
# Copyright Harold Clark 2017
#
try:
    import lib.uasyncio as asyncio
except ImportError:
    import uasyncio as asyncio
from utime import time
import machine
from WaterPumps.events import Event
from WaterPumps.runData import runData
from WaterPumps.validCommands import validCommand

class pump(object):
    def __init__(self, powerPin,startupTime=20, name='Pump'):
        """Init a pump"""
        
        self._name = name
        self.Power = machine.Pin(powerPin,machine.Pin.OUT)
        self.startupTime = startupTime
        self._monitorEvents = []
        self.currentRunData = None
        self.pumpRunData = []
        self.pumpNotReadyEvent = Event(name='Pump Not Ready') # event for pump to know it okay to start
        self.pumpStartEvent = Event(name='Pump Start') # event for services that need to do some in the startup period
        self.pumpRunningEvent = Event(name='Pump Running') # subscriber event for pumpOn
        self.pumpOnEvent = Event(name='Pump On') # cleint event, pumpOn ie button, server, upstream server
        self.pumpOnClients = []
        self.pumpOffEvent = Event(name='Pump Off') # client event, pumpOff ie button, server, downstream
        self.pumpOffClients  = []
        self.pumpTimeOnEvent = Event(name='Pump Time On') # client event, running time ie server
        self.pumpStatusEvent = Event(name='Pump Status')
        self.pumpFinishDataEvents = []
        self._validCommandList = []
        self.registerMonitorEvent('pumpOn', self.pumpOnEvent, self.pumpOn)
        self.registerMonitorEvent('pumpOff',self.pumpOffEvent, self.pumpOff)
        self.registerMonitorEvent('timeOn',self.pumpTimeOnEvent, self.timeOn)
        self.registerMonitorEvent('pumpStatus', self.pumpStatusEvent, self.pumpStatus)
        

    def clearData(self):
        if CurrentRun:
            self.pumpRunData.append(self.currentRunData)
        self.currentRunData = runData()
        
    def name(self):
        return self._name
    
    def validCommandList(self):
        return self._validCommandList


    async def pumpOff(self, event):
        print("""%s - %s: shuting down pump, return event name: %s ...""" % (self._name, time(),event.name()))
        if self.Power.value():
            self.pumpNotReadyEvent.set(True)
            self.Power.value(False)
            self.pumpRunningEvent.clear()
            self.currentRunData.finish = time()
            self.pumpStartEvent.clear()            
            wlist = list(self.pumpOffClients)
            for e in wlist:
                e.set(self.currentRunData)
            await asyncio.ms_sleep(100)
            while len(wlist):                
                for e in wlist:
                    if e.is_set():
                        wlist.remove(e)
                await asyncio.ms_sleep(50)
            self.pumpNotReadyEvent.clear()
            msg ="""Pump Turned off"""
        else:
            msg = """Pump was already off!"""
        print('''%s - %s: %s''' % (self._name, time(), msg))
        event.set(msg)
        #return msg


    async def pumpOn(self, event):
        print("""%s - %s: Starting up pump, return event name %s ...""" % (self._name, time(),event.name()))
        if self.Power.value():
            msg = '''pump is already on, started at %s''' % (self.currentRunData.start)
        else:
            if self.pumpNotReadyEvent.is_set():
                msg = 'Pump not safe to start.'
            else:
                self.clearData()
                self.Power.value(True)
                self.pumpRunningEvent.set(self.currentRunData.start)
                self.pumpStartEvent.set(self.currentRunData.start + self.startupTime)
                events = list(self.pumpOnClients)
                for event in events:
                    event.set(Event())
                while len(events):
                    await asyncio.ms_sleep(50)
                    for event in events:
                        if not event.is_set():
                            events.remove(event)
                msg = """Pump Turned On"""
        print('''%s - %s: %s''' % (self._name,self.currentRunData.start,msg))
        print('''%s - %s: pump on, value of start event: %s''' % (self.pumpStartEvent._name, time(), self.pumpStartEvent.value()))
        event.set(msg)
        return msg    
        
    async def pumpStatus(self, event):
        """check status of pump, and return test"""
        if self.Power.value():
            timeOn = Event(name='Time On')
            self.pumpTimeOnEvent.set(timeOn)
            await timeOn
            msg = """Pump is on, running time: %s""" % (timeOn.value())
        else:
            msg = """Pump is off."""
        event.set(msg)
        #return msg
        
    async def timeOn(self, event):
        if self.pumpRunningEvent.is_set():
            TimeOn = str(time() - self.currentRunData.start)
        else:
            if self.currentRunData:
                TimeOn = '''Pump is Off, last run: %s''' % (self.currentRunData.finsh - self.currentRunData.start)
            else:
                TimeOn = 'Pump is off'
        event.set(TimeOn)
        return TimeOn
            
        
    def registerMonitorEvent(self, name, event, func):
        if name:
            self._validCommandList.append(validCommand(name, event))
        self._monitorEvents.append((Event, func))
            
    def registerPumpOn(self, event=None):
        if event:
            self.pumpOnClients.append(event)
        return self.pumpOnEvent
    
    def registerPumpOff(self, event=None):
        if event:
            self.pumpOffClients.append(event)
        return self.pumpOffEvent
    
    #def registerFinishDataEvent(self, event):
    #    self.pumpFinishDataEvents.append(event)
    #    return self.pumpFinishEvent
    
            
    async def monitorPump(self, debug=False):
        """coroutine for handling pump requests"""
        print('''%s - %s: Monitor of pump started''' % (self._name, time()))
        loopcount = 0
        while True:
            loopcount += 1 
            await asyncio.sleep_ms(50)
            if debug:
                print('''%s - %s: loop count: %s''' % (self._name, time(), loopcount))
            for event, func in self._monitorEvents:
                if event.is_set():
                    mainLoop = asyncio.get_event_loop()
                    mainLoop.create_task(func(event.value()))
                    print('''%s - %s: added %s to loop %s''' % (self._name, time(), event._name, func))
                    event.clear()