# Author: Harold Clark
# Copyright Harold Clark 2017
#
import machine
import time
import uasyncio.core as asyncio

class flowMeter(object):
    def __init__(self, flowPin, flowCount=0, rate=7.5):
        """Init a Flow meter sensor object"""
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
        if self.timeDelta!=0:
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
        
    
    async def monitorFlowMeter(self, count):
        """coroutine for monitoring flow"""
        
        while True:
            #if flowCount>0:
            #    self.setFlowCount(flowCount)
            #    flowCount = 0
            #    Hz = self.calculateflow()
            #    totalseconds = time.time() - self.flowStartTime
            #    totalliters = self.totalFlowCount/450
            
            print("""MonitroFlowMeter count: %s""" % (count))
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
        