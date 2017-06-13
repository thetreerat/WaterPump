# Author: Harold Clark
# Copyright Harold Clark 2017
#

try:
    import uasyncio.cor as asyncio
except ImportError:
    import lib.uasyncio.core as asyncio
    
import machine
from utime import time
from WaterPumps.events import Event
from WaterPumps.validCommands import validCommand
from WaterPumps.runData import runData

class valve(object):
    def __init__(self, valvePin, name='Valve'):
        self._name = name
        self.valvePower = machine.Pin(valuePin)
        self.valveOnEvent = Event(name='''%s On Event''' % (self._name))
        self.valveOnClients = []
        self.valveOffEvent = Event(name='''%s Off Event''' % (self._name))
        self.valveOffClients = []
        self.valveStatus = Event(name='''%s valve status event''' % (self._name))
        self.timeOnEvent = Event(name='''%s time On Event''' % (self._name))        
        self.valveFlow = Event(name='''%s Flow On''' % (self._name))
        self.currentRun = None
        self.runData = []
        self.valveOnReadyEvent = Event(name='''%s valve ready''' % (self._name))
        self.valveOnReadyEvent.set(time())
        self._valveMonitorEvents = []
        self.registerMonitorEvent('valveOn', self.valveOnEvent, self.valveOn)
        self.registerMonitorEvent('valveOff', self.valveOffEvent, self.valveOff)
        self.registerMonitorEvent('valveStatus', self.valveStatusEvent, self.valveStatus)
        self.registerMonitorEvent('timeOn', self.timeOnEvent, self.timeOn)
        self._validCommandList = []

    def name(self):
        return self._name
    
    def clearData(self):
        if CurrentRun:
            self.runData.append(self.currentRun)
        self.currentRun = runData()
        
    def registerFlow(self):
        return self.valveFlow
    
    def registerValveOn(self, event):
        if event:
            self.valveOnClients.append(event)
        return self.valveOnEvent()
    
    def registerValveOff(self, event):
        if event:
            self.valveOffCleints.append(event)
        return self.valveOnEvent
    
    def registerMonitorEvent(self, name, event, func):
        self._validCommandlist.append(validCommand(Name, event))
        self._valveMonitorEvents.append((Event, func))
        
    async def valveOn(self, rEvent):
        if self.valvePower.value():
            rEvent.set('Valve already Open')
        else:
            await self.valveOnReadyEvent.is_set()
            self.ClearData()
            self.valvePower.value(True)
            self.valveFlowEvent.set(time())
            self.valveOnReadyEvent.clear()
            wlist = list(self.valveOnClients)
            for l in wlist:
                l.set(time())
            await asyncio.sleep_ms(100)
            while len(wlist):
                for l in wlist:
                    if not l.is_set():
                        wlist.remove(l)
                        await asyncio.sleep_ms(50)
            rEvent.set('''%s valve on at %s''' % (self._name, time()))
        
    
    async def valveOff(self, rEvent):
        if self.valvePower.value():
            self.valvePower.value(False)
            self.valveFlowEvent.clear()
            elist = list(self.valveOffClients)
            for e in elist:
                e.set(time())
            while len(elist):
                for e in elist:
                    await async.sleep_ms(50)
                    if e.is_set():
                        elist.remove(e)
            self.valveOnReadyEvent.set()
            rEvent.set('Valve off Now!!')
        else:
            rEvent.set('Valve was off')
    
    def validCommandList(self):
        return self._validCommandList
    
    async def monitorValve(self):
        print('''%s -%s: Valve Monitor Started''' % (self.name(),time())
        while True:
            await asyncio.sleep_ms(50)
            for event, func in self._valveMonitorEvents:
                if event.is_set():
                    mainLoop = asyncio.get_event_loop()
                    mainLoop.create_task(func(event.value()))
                    print('''%s - %s: event %s set, adding func %s to loop''' % (self._name, time(), event.name(), func))
                    event.clear()
                
        
    