# Author: Harold Clark
# Copyright Harold Clark 2017
#
import machine
import time
try:
    import uasyncio.core as asyncio
except ImportError:
    import lib.uasyncio.core as asyncio
from WaterPumps.events import Event
from WaterPumps.validCommands import validCommand
flowCount =0


class flowMeter(object):
    GALLON_LITTER = 0.264172
    ADAFRUIT_1_2_PULSE_LITTER = 450
    ADAFRUIT_1_2_RATE = 7.5
    G1_PULSE_LITTER = 450
    G1_RATE = 4.5
    
    def __init__(self, flowPin, flowCount=0, rate=7.5, name='flowMeter', clicks=450):
        """Init a Flow meter sensor object"""
        self._name = name
        self.counterPin = machine.Pin(flowPin, machine.Pin.IN)
        self.flowCount = flowCount
        self.currentTime = self.timeInMillaseconds()
        self.lastTime = self.timeInMillaseconds()
        self.rate = rate
        self.flowStartTime = time.time()
        self.totalFlowCount = 0
        self.currentFlow = 0
        self.flowRate = 0
        self.gallonLiter = self.GALLON_LITTER
        self.noFlowEvent = Event(name='''%s No Flow''' % (self._name)) # 
        #self.finishEvent = Event(name='Finish Event with no handle') # should be a handle to a foreign event
        self.shutoffComplete = Event(name='shutoff event with rundata payload')
        self.currentFlowEvent = Event(name='%s Current Flow')
        self.runningEvent = False # should be a handle to a foreign event
        self.startupEvent = False
        self.clicksToLiters = clicks
        self._validCommandList = []
        self._monitorEvents = []
        self.registerMonitorEvent('currentFlow', self.currentFlowEvent, self.currentFlow)
        self.registerMonitorEvent('runningTotal', self.runningTotal, self.runningTotal)
        
    def calculateFlow(self, debug=False):
        """Calucate the instatane flow"""
        if self.timeDelta()!=0:
            Hz = (self.flowCount/self.timeDelta())
        else:
            Hz = 0
        self.flowRate = (Hz / self.rate) # liters per minute
        if debug:
            print("Debug mode on:")
            print("""Hertz: %s""" % (Hz))
            print("""instant flow count: %s""" % (self.flowCount))
            print("""time Delta: %s""" % (self.timeDelta()))
            print("end debug message")
        return Hz
        #self.currenttime = self.timeInMillaseconds()

    def launch(self, monitorObject):
        m = monitorObject
        mainLoop = asyncio.get_event_loop()
        mainLoop.create_task(m.func(**m.args))
        
    def name(self):
        return self._name
    
    
    def registerRunningEvent(self, event):
        self.runningEvent = event
        return 1
    
    def registerStartupEvent(self, event):
        self.startupEvent = event
        return 1
        
    def registerShutOff(self):
        self.registerMonitorEvent(None, self.shutOffComplete, self.getFinishData)
        return self.shutOffComplete
        
    def registerMonitorEvents(self, name, event, func, args={}):
        if name:
            self._validCommandList.append(validCommand(name, event))
        self._monitorEvents.append((Event, func))
        
    #def registerFinishEvent(self, event=None):
    #    if registerFinishEvent:
    #        self.finishEvent = event
    #    return self.shutoffDataReturn


    def setFlowCount(self,flowCount):
        """set flowCount and reset time var"""
        self.flowCount = flowCount
        self.lastTime = self.currentTime
        self.currentTime = self.timeInMillaseconds()
        self.totalFlowCount += self.flowCount
        
        
    def timeDelta(self):
        """calculate time delta in millaseconds"""
        delta = time.ticks_diff(self.currentTime, self.lastTime)/1000
        return delta


    def timeInMillaseconds(self):
        timevalue =  time.ticks_ms()
        return timevalue
    

    def validCommandList(self):
        """return a list of valid server commands. if a fuction not to be exposed to server don't list"""
        for c in self.validCommandList:
            l.append(c.name())
        return l

    async def currentFlow(self):
        if self.runningEvent.is_set():
            self.currentFlowEvent.value().set(self.flowRate)
        else:
            self.currentFlowEvent.value().set('Pump is Off')

    async def getFinishData(self):
        totalFlow = self.totalFlowCount / self.clicksToLiters
        print('''%s - %s: Total Liters: %s''' % (self._name,time.time(),totalFlow))                
        self.shutOffEvent.value().totalLiters = totalflow
        self.totalFlowCount = 0
                
            
    async def monitorFlowMeter2(self, debug=False):
        print('''%s -%s: Monitor of flow meter started''' % (self._name, time.time()))
        global flowCount
        self.noFlowEvent.clear()
        flowCount = 0
        if not self.runningEvent:
            self.runningEvent = Event()
            self.runningEvent.set()
        while True:
            await asyncio.ms_sleep(50)
            if flowCount>0:
                self.noFlowEvent.clear()
                self.setflowCount(flowCount)
                flowCount = 0
                Hz = self.calculateFlow()
                print("""%s - %s: %s LPM""" % (self._name, time.time(), self.flowRate))
            else:
                if self.startupEvent:
                    if self.startupEvent.value() > time():
                        self.noFlowEvent.set(time())
            for m in self._moitorEvents:
                if m.event.is_set():
                    self.launch(m)
                    m.event.clear()
            
                
            
    async def monitorFlowMeter(self, debug=False):
        print('''%s -%s: Monitor of flow meter started''' % (self._name, time.time()))
        global flowCount
        self.noFlowEvent.clear()
        flowCount = 0
        if not self.runningEvent:
            self.runningEvent = Event()
            self.runningEvent.set()
        while True:
            if self.runningEvent.is_set():
                if flowCount>0:
                    self.noFlowEvent.clear()
                    self.setFlowCount(flowCount)
                    flowCount = 0
                    Hz = self.calculateFlow()
                    #totalseconds = time.time() - self.flowStartTime
                    #totalliters = self.totalFlowCount/450
            
                    print("""%s - %s: %s LPM""" % (self._name, time.time(), self.flowRate))
                else:
                    if not self.noFlowEvent.is_set() and flowCount==0:
                        self.noFlowEvent.set(time.time())
                        if debug:
                            print('''%s - %s: flowCount: %s''' % (self._name, time.time(), flowCount))
                    if debug:
                        print('''%s - %s: No flow - Event: %s value: %s''' % (self._name, time.time(), self.noFlowEvent._name, self.noFlowEvent.value()))
            elif self.finishEvent.is_set() and flowCount>0:
                self.noFlowEvent.clear()
                self.setFlowCount(flowCount)
                
            await asyncio.sleep_ms(50)
            if self.finishEvent.is_set() and flowCount==0:
                totalFlow = self.totalFlowCount / self.clicksToLiters
                print('''%s - %s: Total Liters: %s''' % (self._name,time.time(),totalFlow))                
                self.flowFinishData.set(totalFlow)
                self.totalFlowCount = 0
            if self.startupEvent and self.shutOffEvent:
                if self.startupEvent.is_set():
                    if self.startupEvent.value() < time.time() and not self.shutOffEvent.is_set() and self.noFlowEvent.is_set():
                        print('''startupEvent value: %s, posting ''' % (self.startupEvent.value()))        
                        self.shutOffEvent.set(self.shutoffDataReturn)
            if debug:
                if self.noFlowEvent==None:
                    print('no finishEvent handle')
                else:
                    print('''%s - %s: Finish Event set: %s, value: %s''' % (self._name, time.time(), self.finishEvent.is_set(),self.finishEvent.value()))
            if self.shutoffDataReturn.is_set():
                self.shutoffDataReturn.clear()            
            if self.currentFlowEvent.is_set():
                if self.runningEvent.is_set():
                    self.currentFlowEvent.value().set(self.flowRate)
                else:
                    self.currentFlowEvent.value().set('Pump is Off')
                self.currentFlowEvent.clear()
            await asyncio.sleep_ms(300)


def callbackflow(p, debug=False):
    """Add on to Counter """
    global flowCount
    flowCount += 1
    if debug:
        print("""callback count: %s""" % (flowCount))        
        