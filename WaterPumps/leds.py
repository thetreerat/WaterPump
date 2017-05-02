# Author: Harold Clark
# Copyright Harold Clark 2017
#
class led(object):
    def __init__(self,ledPin=0):
        """Init a single color led object"""
        import machine
        self.powerPin = machine.Pin(ledPin, machine.Pin.OUT)


class triLed(object):
    def __init__(self, redpin, bluepin, greenpin,name='Test', startColor=None):
        """Init a Tri color led object"""
        import machine
        self.redPin = machine.Pin(redpin, machine.Pin.OUT)
        self.bluePin = machine.Pin(bluepin, machine.Pin.OUT)
        self.greenPin = machine.Pin(greenpin, machine.Pin.OUT)
        self.ledServerList  = []
        self._name = name
        if startColor==None:
            self.turnOff
        else:
            startColor()
        
    def name(self):
        return self._name
    
    
    def registerLedClient(self, testTuple, index=0, debug=False):
        if len(testTuple)==3:
            self.ledServerList.insert(index, testTuple)
            if debug:
                print(len(self.ledServerList))
                print(self.ledServerList[-1])
        
    async def monitorLED(self):
        """coroutine for monitor event to change the LED color"""
        import uasyncio as asyncio
        from utime import time
        print('''%s - %s: monitorLED Started''' % (self.name(), time()))
        while True:
            
            for pair, func, clear in self.ledServerList:
                v = True
                for event, test in pair:
                    v = event()==test and v
                if v:
                    mainLoop = asyncio.get_event_loop()
                    mainLoop.create_task(func())
                    print('added task to loop')
                    if clear!=None:
                        clear.clear()
                    break
            await asyncio.sleep_ms(50)
            
    def setColor(self, color):
        """set TriColor LED to pass color (RBG)"""
        R, B, G = color
        self.redPin.value(R)
        self.bluePin.value(B)
        self.greenPin.value(G)
        
    def makeGreen(self):
        """Turn Tri Color LED Green"""
        #value(True) = off, vaule(False) = on
        self.redPin.value(True)
        self.greenPin.value(False)
        self.bluePin.value(True)
    
    
    def makeRed(self):
        """ Turn Tri Color LED Red"""
        self.redPin.value(False)
        self.greenPin.value(True)
        self.bluePin.value(True)
        
    
    async def makeBlue(self):
        """ Turn Tri Color LED Red"""
        self.redPin.value(True)
        self.greenPin.value(True)
        self.bluePin.value(False)


    def makeYellow(self):
        """ Turn Tri Color LED off"""
        self.redPin.value(False)
        self.greenPin.value(False)
        self.bluePin.value(True)
 
 
    def makeWhite(self):
        """Trun Tri Color LED White"""
        self.redPin.value(False)
        self.greenPin.value(False)
        self.bluePin.value(False)
        
    def makeOrange(self):
        """Turn tri color LED Orange"""
        self.redPin.value(False)
        self.bluePin.value(False)
        self.greenPin.value(True)
        
    def turnOff(self):
        """ Turn Tri Color LED off"""
        self.redPin.value(True)
        self.greenPin.value(True)
        self.bluePin.value(True)
        
    async def flashBlue(self):
        self.flash(self.makeBlue)
    
    async def flash(color=None):
        if color==None:
            color=self.makeRed()
        while True:
            color()
            await asyncio.sleep_ms(100)
            self.turnOff()
            await asyncio.sleep_ms(100)