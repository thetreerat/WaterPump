# Author: Harold Clark
# Copyright Harold Clark 2017
#


class pump(object):
    def __init__(self, powerPin,startupTime=20, name='Pump'):
        """Init a pump"""
        import machine
        from WaterPumps.events import Event
        self._name = name
        self.Power = machine.Pin(powerPin,machine.Pin.OUT)
        self.startupTime = startupTime
        self.pumpClients = []
        self.pumpServers = []
        self.pumpMonitorEvents = []
        self.currentRunData = None
        self.pumpRunData = []
        self.pumpNotReadyEvent = Event(name='Pump Not Ready') # event for pump to know it okay to start
        self.pumpStartEvent = Event(name='Pump Start') # event for services that need to do some in the startup period
        self.pumpCleanUpEvent = Event(name='Cleanup run data')
        self.pumpFinishEvent = Event(name='Pump Finish',debug=True) # event for service that need to supply data 
        self.pumpRunningEvent = Event(name='Pump Running') # subscriber event for pumpOn
        self.pumpOnEvent = Event(name='Pump On') # cleint event, pumpOn ie button, server, upstream server
        self.pumpOffEvent = Event(name='Pump Off') # client event, pumpOff ie button, server, downstream
        self.pumpTimeOnEvent = Event(name='Pump Time On') # client event, running time ie server
        self.pumpStatusEvent = Event(name='Pump Status')
        self.pumpFinishDataEvents = []
        self.registerMonitorEvent(self.pumpOnEvent, self.pumpOn)
        self.registerMonitorEvent(self.pumpOffEvent, self.pumpOff)
        self.registerMonitorEvent(self.pumpTimeOnEvent, self.timeOn)
        self.registerMonitorEvent(self.pumpStatusEvent, self.pumpStatus)
        self.registerMonitorEvent(self.pumpCleanUpEvent, self.pumpFinish)
        

        
    def name(self):
        return self._name
    
    async def pumpOn(self, event):
        """Turn on Pump if off. print and return action proformed"""
        from utime import time
        from WaterPumps.pumpRunData import pumpRunData
        if not self.Power.value() and not self.pumpNotReadyEvent.is_set():
            self.pumpRunData.append(self.currentRunData)
            self.currentRunData = pumpRunData()
            self.Power.value(True)
            self.pumpRunningEvent.set(self.currentRunData.start)
            self.pumpFinishEvent.clear()
            self.pumpNotReadyEvent.clear()
            self.pumpStartEvent.set(self.currentRunData.start + self.startupTime)
            msg = """Pump Turned On"""
        elif self.Power.value():
            msg = """pump is already on!"""
        elif self.pumpNotReadyEvent.is_set():
            msg = 'Pump not safe to start.'
        else:
            msg = 'pump in unknown state'
        print('''%s - %s: %s''' % (self._name,self.currentRunData.start,msg))
        return msg
    
    
    async def pumpOff(self, event):
        """Turn off pump if on. prints action proformed and return action as string"""
        from utime import time
        print("""%s - %s: shuting down pump ...""" % (self._name, time()))        
        if self.Power.value():
            self.Power.value(False)
            
            self.currentRunData.finish = time()
            print('setting finish event')
            self.pumpFinishEvent.set(self.currentRunData.finish)
            print('''%s, %s''' % (self.pumpFinishEvent.is_set(),self.pumpFinishEvent.value()))
            self.pumpOnEvent.clear()
            self.pumpStartEvent.clear()
            self.pumpRunningEvent.clear()
            self.pumpNotReadyEvent.set(True)
            msg ="""Pump Turned off"""
        else:
            msg = """Pump was already off!"""
        print('''%s - %s: %s''' % (self._name, self.pumpFinishEvent.value(), msg))
        event.set(msg)
        return msg
        
        
    async def timeOn(self, event):
        import time
        if self.powerOnTime:
            TimeOn = str(time.time() - self.powerOnTime)
        else:
            TimeOn = 'Pump is Off'
        event.set(TimeOn)
        return TimeOn
    
    
    async def pumpStatus(self, event):
        """check status of pump, and return test"""
        from WaterPumps.server_uasyncio import Event
        if self.Power.value():
            msg = """Pump is on, running time: %s""" % (self.timeOn())
        else:
            msg = """Pump is off."""
        event.set(msg)
        return msg

    async def pumpFinish(self, event):
        """coroutine for saving data"""
        print('Data will not be saved!!')
        import uasyncio as asyncio
        events = self.pumpFinishDataEvents
        while len(events)!=0:
            for e,s in events:
                if e.is_set():
                    if s=='pumpedTotal':
                        self.currentRunData.pumpedTotal = e.value()
                    e.clear()
                    events.remove((e,s))
            await asyncio.sleep_ms(50)
        self.pumpNotReadyEvent.clear()
        self.pumpFinishEvent.clear()
            
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
        
        
    def registerMonitorEvent(self, Event, func):
        self.pumpMonitorEvents.append((Event, func))
        
        
    def registerPumpClient(self, name):
        """register client to pump monitor and return valid Event handles"""
        self.pumpClient.append(name)
        return self.validCommandList()
    
    def registerPumpServer(self, name):
        self.pumpServers.append(name)
        e = []
        e.append(('pumpStartEvent', self.pumpStartEvent))
        e.append(('pumpRunningEvent', self.pumpRunningEvent))
        e.append(('pumpFinishEvent', self.pumpFinishEvent))
        e.append(('pumpNotReadyEvent', self.pumpNotReadyEvent))
        return e
    
    def registerFinishDataEvent(self, event, store):
        self.pumpFinishDataEvents.append((event,store))
            
    async def monitorPump(self, debug=False):
        """coroutine for handling pump requests"""
        from utime import time
        import uasyncio as asyncio
        print('''%s - %s: Monitor of pump started''' % (self._name, time()))
        loopcount = 0
        while True:
            loopcount += 1
            await asyncio.sleep_ms(50)
            if debug:
                print('''%s - %s: loop count: %s''' % (self._name, time(), loopcount))
            for event, func in self.pumpMonitorEvents:
                if event.is_set():
                    mainLoop = asyncio.get_event_loop()
                    mainLoop.create_task(func(event.value()))
                    print('''%s - %s: added %s to loop %s''' % (self._name, time(), event._name, func))
                    event.clear()
            
           