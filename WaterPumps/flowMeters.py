# Author: Harold Clark
# Copyright Harold Clark 2017
#
import machine
import time

import uasyncio.core as asyncio
    
flowCount =0
from WaterPumps.events import Event

class flowMeter(object):
    def __init__(self, flowPin, flowCount=0, rate=7.5, name='flowMeter', clicks=450):
        """Init a Flow meter sensor object"""
        self._name = name
        self.counterPin = machine.Pin(flowPin, machine.Pin.IN)
        self.flowCount = flowCount
        self.currentTime = self.timeInMillaseconds()
        self.lastTime = self.currentTime
        self.rate = rate
        self.flowStartTime = self.timeInMillaseconds()
        self.totalFlowCount = 0
        self.currentFlow = 0
        self.flowRate = 0
        self.gallonLiter = 0.264172
        self.noFlowEvent = Event(name='No Flow')
        self.pumpFinishEvent = None
        self.flowFinishData = Event()
        self.RunningEvent = None
        self.clicksToLiters = clicks

        
    def timeInMillaseconds(self):
        timevalue = int(time.time())
        return timevalue
    
    def setFlowCount(self,flowCount):
        """set flowCount and reset time var"""
        self.flowCount = flowCount
        self.lastTime = self.currentTime
        self.currentTime = self.timeInMillaseconds()
        self.totalFlowCount += self.flowCount
        
    def timeDelta(self):
        """calculate time delta in millaseconds"""
        delta = self.currentTime - self.lastTime
        return delta

        
    def calculateflow(self, debug=False):
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


    def validCommandList(self):
        """return a list of valid server commands. if a fuction not to be exposed to server don't list"""
        list = []
        list.append(validCommand('calculateflow',self.calculateflow))
        return list
        
    
    async def monitorFlowMeter(self, debug=False):
        """coroutine for monitoring flow"""
        global flowCount
        self.noFlowEvent.clear()
        flowCount += 1
        print('''%s -%s: Monitor of flow meter started''' % (self._name, time.time()))
        if self.RunningEvent==None:
            self.RunningEvent = Event()
            self.RunningEvent.set()
        while True:
            if self.RunningEvent.is_set():
                if flowCount>0:
                    self.noFlowEvent.clear()
                    self.setFlowCount(flowCount)
                    flowCount = 0
                    Hz = self.calculateflow()
                    #totalseconds = time.time() - self.flowStartTime
                    #totalliters = self.totalFlowCount/450
            
                    print("""%s - %s: %s LPM""" % (self._name, time.time(), self.flowRate))
                else:
                    if self.flowRate==0 and not self.noFlowEvent.is_set():
                        self.noFlowEvent.set(time.time())
                    if debug:
                        print('''%s - %s: No flow - Event: %s value: %s''' % (self._name, time.time(), self.noFlowEvent._name, self.noFlowEvent.value()))
            if self.pumpFinishEvent.is_set() and flowCount==0:
                totalFlow = self.totalFlowCount / self.clicksToLiters
                print('''%s - %s: Total Liters: %s''' % (self._name,time.time(),totalFlow))
                self.flowFinishData.set(totalFlow)
                self.totalFlowCount = 0
            if debug:
                if self.noFlowEvent==None:
                    print('no pumpFinishEvent handle')
                else:
                    print('''%s - %s: Finish Event set: %s, value: %s''' % (self._name, time.time(), self.pumpFinishEvent.is_set(),self.pumpFinishEvent.value()))
            await asyncio.sleep(2)

class flowRunData(object):
    """Class for create object to store Data"""
    def __init__(self, clicks=450):
        """init of data object"""
        self.startTime = time.time()
        self.endTime = 0
        self.totalCount = 0
        self.clicksToLiters = clicks

        
    def totalRunTime(self):
        """Calulate Run Time"""
        if self.endTime==0:
            runtotal = time.time() - self.startTime
        else:
            runtotal = self.endTime - self.startTime
        return runtotal
    
    
    def totalFlow(self, Liters=True):
        """Calculate total flow from total Clicks"""
        flow = self.totalCount / self.clicksToLiters
        if not Liters:
            flow = flow * 0.264172 # convert liters to gallons
        return flow
    
    def averageFlowRate(self):
        """calculate average flow rate for the run"""
        return (self.clicksToLiters/self.totalRunTime)/60

def callbackflow(p, debug=False):
    """Add on to Counter """
    global flowCount
    flowCount += 1
    if debug:
        print("""callback count: %s""" % (flowCount))        
        