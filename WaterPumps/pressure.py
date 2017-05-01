# Author: Harold Clark
# Copyright Harold Clark 2017
#
import machine
import time
import uasyncio.core as asyncio

class pressureSensor(object):
    """ Class for pressure sensor """
    def __init__(self, pin=0, LowPressure=20, highPressure=150, cutoffPressure=170):
        """init a pressure sensor on pin x"""
        from WaterPumps.server_uasyncio import Event
        self.name = 'PressureSensor'
        self.pressure = machine.ADC(pin)
        self.avgRaw = self.avgread()
        self.psi = self.convertValue(self.avgRaw)
        self.maxPsi = 0
        self.lowPressure = 20
        self.highPressure = 150
        self.cutoffPressure = 170
        self.sensorLowCorrection = 101
        self.ADCPressureConstence = .1708
        self.lastPSI = 0
        self.pump = False
        self.statusLED = False
        self.pressureHighEvent = Event()
        self.

    

    def avgread(self):
        """ read sensor 3 times and average """
        c = 0
        p = 0
        while c < 3:
            p = p + self.pressure.read()
            time.sleep(.1)
            c += 1
        p = p/3
        
        return p
    
    
    async def checkPressure(self, event, debug=True):
        event.set(self.readPressure())
        if debug:
            print("""checkPressure msg: %s """ % (event.value()))
        await asyncio.sleep(4)
        
    
    
    def currentPSI(self):
        """read Avg valuse convert to psi and set self.PSI and event data"""
        self.avgRaw = self.avgread()
        self.psi = self.convertValue(self.avgRaw)
        if self.psi < 0:
            self.psi = 0
        return self.psi


    def readPressure(self):
        msg = 'not read'
        psi = self.currentPSI()
        if psi>self.maxPsi:
            self.maxPsi = psi                
        if psi<self.lowPressure and self.lastPSI!=psi:
            msg = """Low Pressure warning: %s""" % (psi)
        elif psi>self.highPressure and psi<self.cutoffPressure:
            msg = """High Pressure warning: %s""" % (psi)
        elif psi>self.cutoffPressure:
            msg = """Dangerous Pressure: %s, Shut Down Pump!!!""" % (psi)
            if self.pump:
                msg = """Shutdown pump, Pressure over uppper limit: %s""" % (psi)
                self.pump.pumpOff(self.statusLED)
            if self.statusLED:
                self.statusLED.makeRed()
        else:
            msg = """%s reading: %s""" % (self.name, psi)
        self.lastPSI = psi            
        return msg
    
    async def MonitorPressure(self, event=False):
        """check values and print warning if needed"""
        if not event:
            event = self.event
        while True:
            msg = False
            if self.pump:
                if self.pump.Power.value():
                    msg = self.readPressure()
            else:
                msg = self.readPressure()
            if msg:
                print(msg)
            await asyncio.sleep(2)
    
    def convertValue(self, v):
        """ convert value to PSI """
        psi = round((v - 101) * .1708)
        return psi
    
    def CalibrateSensor(self, event):
        """This sets the sensorLowCorrection value, this should only be run when there is
           no pressure on the sensor as it will adjust what is a 0 psi reading"""
        self.sensorLowCorrection = round(self.avgread())
        event.set("""sensorLowCorrection set to %s""" % (self.sensorLowCorrection))
        print(event.value())
        
        
    def validCommandList(self):
        """return a list of valid server commands. if a fuction not to be exposed to server don't list"""
        from WaterPumps.server_uasyncio import validCommand
        list = []
        list.append(validCommand('CalibrateSensor',self.CalibrateSensor))
        list.append(validCommand('checkPressure',self.checkPressure))
        return list
        #[, 'currentPSI'] # MaxPSI
        