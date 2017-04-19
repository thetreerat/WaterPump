import machine
import time
import uasyncio.core as asyncio

class pump(object):
    """Pump oject"""
    def __init__(self, powerPin,startupTime=20):
        """Init a pump"""
        self.Power = machine.Pin(powerPin,machine.Pin.OUT)
        self.powerOnTime = 0
        self.flow = False
        self.ledColor = (True,False,True) #Blue
        self.startupTime = startupTime
        
        
    async def pumpOn(self, statusLED):
        """Turn on Pump if off. print and return action proformed"""
        if not self.Power.value():
            self.Power.value(True)
            msg = """Pump Turned On"""
            
            self.powerOnTime = time.time()
            self.ledColor = (False,False,False) # White
            statusLED.setColor(self.ledColor)
        else:
            msg = """pump is already on!"""
        print(msg)
        return msg
        await asyncio.sleep_ms(50)
    
    
    async def pumpOff(self, statusLED):
        """Turn off pump if on. prints action proformed and return action as string"""
        print("""shuting down pump ...""")
        if self.Power.value():
            self.Power.value(False)
            msg ="""Pump Turned off"""
            self.powerOnTime = 0
            self.ledColor = (True, False, True)
            statusLED.setColor(self.ledColor)
        else:
            msg = """Pump was slready off!"""
        print(msg)
        return msg
        await asyncio.sleep_ms(50)
        
        
    async def timeOn(self):
        TimeOn = time.time() - self.powerOnTime
        return TimeOn
        await asyncio.sleep_ms(50)
    
    
    async def pumpStatus(self):
        """check status of pump, and return test""" 
        if self.Power.value():
            msg = """Pump is on, running time: $s""" % (self.powerOnTime())
        else:
            msg = """Pump is off."""
        await asyncio.sleep(1)    
            
    def validCommandList(self):
        """return a list of valid server commands. if a fuction not to be exposed to server don't list"""
        return ['pumpOn', 'pumpOff', 'pumpStatus', 'timeOn']
        
