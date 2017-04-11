import machine
import time

class pump(object):
    """Pump oject"""
    def __init__(self, powerPin,startupTime=20):
        """Init a pump"""
        self.Power = machine.Pin(powerPin,machine.Pin.OUT)
        self.powerOnTime = 0
        self.flow = False
        self.ledColor = (True,False,True) #Blue
        self.startupTime = startupTime
        
        
    def pumpOn(self, statusLED):
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
    
    
    def pumpOff(self, statusLED):
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
        
    def timeOn(self):
        TimeOn = time.time() - self.powerOnTime
        return TimeOn
    
    
    def pumpStatus(self):
        """check status of pump, and return test""" 
        if self.Power.value():
            msg = """Pump is on, running time: $s""" % (self.powerOnTime())
        else:
            msg = """Pump is off."""
            
            
    def validCommandList(self):
        """return a list of valid server commands. if a fuction not to be exposed to server don't list"""
        return ['pumpOn', 'pumpOff', 'pumpStatus', 'timeOn']
        
        
    #def serverRequest(self, command):
    #    """function to reform remote connection request and retrun status of command"""
    #    statis = "hello"
    #    return stats