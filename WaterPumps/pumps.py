import uasyncio.core as asyncio
from WaterPumps.server_uasyncio import validCommand

class pump(object):
    def __init__(self, powerPin,startupTime=20, statusLED=False):
        """Init a pump"""
        import machine
        self.Power = machine.Pin(powerPin,machine.Pin.OUT)
        self.powerOnTime = False
        self.flow = False
        self.ledColor = (True,False,True) #Blue
        self.statusLED = statusLED
        self.startupTime = startupTime
        self.runList = []
        self.currentRun = False
        
        
    async def pumpOn(self, event):
        """Turn on Pump if off. print and return action proformed"""
        from utime import time
        from WaterPump.pumpRun import pumpRun
        if not self.Power.value():
            self.Power.value(True)
            msg = """Pump Turned On"""
            self.currentRun = pumpRun()
            self.powerOnTime = time()
            if self.statusLED:
                self.statusLED.setYellow()
        else:
            msg = """pump is already on!"""
        print(msg)
        event.set(msg)
        return msg
        await asyncio.sleep_ms(50)
    
    
    async def pumpOff(self, event):
        """Turn off pump if on. prints action proformed and return action as string"""
        from utime import time
        print("""shuting down pump ...""")        
        if self.Power.value():
            self.Power.value(False)
            self.currentRun.finish = time()
            self.currnetRun.
            
            self.runlist.append(self.currentRun)
            self.currentRun = None
            msg ="""Pump Turned off"""
            self.powerOnTime = False
            if self.statusLED:
                self.makeBlue()
                self.statusLED.setColor(self.ledColor)
            
        else:
            msg = """Pump was already off!"""
        print(msg)
        event.set(msg)
        return msg
        await asyncio.sleep_ms(50)
        
        
    async def timeOn(self, event):
        import time
        if self.powerOnTime:
            TimeOn = str(time.time() - self.powerOnTime)
        else:
            TimeOn = 'Pump is Off'
        event.set(TimeOn)
        return TimeOn
        await asyncio.sleep_ms(50)
    
    
    async def pumpStatus(self,event):
        """check status of pump, and return test"""
        from WaterPumps.server_uasyncio import Event
        if self.Power.value():
            msg = """Pump is on, running time: %s""" % (self.powerOnTime())
        else:
            msg = """Pump is off."""
        event.set(msg)
        await asyncio.sleep(1)    
            
    def validCommandList(self):
        """return a list of valid server commands. if a fuction not to be exposed to server don't list"""
        list = []
        b = validCommand('pumpOn',self.pumpOn)
        list.append(b)
        b = validCommand('pumpOff',self.pumpOff)
        list.append(b)
        b = validCommand('pumpStatus',self.pumpStatus)
        list.append(b)
        b = validCommand('timeOn',self.timeOn) 
        list.append(b)
        return list
        
