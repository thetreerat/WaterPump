# Author: Harold Clark
# Copyright Harold Clark 2017
#
import machine
import time
try:
    import lib.uasyncio.core as asyncio    
except ImportError:
    import uasyncio.core as asyncio

class pressureSensor(object):
    """ Class for pressure sensor """
    def __init__(self, cv, pin=0, LowPressure=20, highPressure=150, cutoffPressure=170, name='PressureSensor'):
        """init a pressure sensor on pin x"""
        from WaterPumps.events import Event
        self._name = name
        self.pressure = machine.ADC(pin)
        self.avgRaw = self.avgread()
        self.psi = self.convertValue(self.avgRaw)
        self.maxPsi = 0
        self.lowPressure = 20
        self.highPressure = 100
        self.cutoffPressure = 150
        self.sensorLowCorrection = 101
        self.ADCPressureConstence = .1708
        self.lastPSI = 0
        self.runningEvent = None
        self.runFinishEvent = None
        self.pressureLowEvent = Event(name='''%s Low Pressure''' % (self._name))
        self.pressuerLowCleints = []
        self.pressureHighEvent = Event(name='''%s Low Pressure''' % (self._name))
        self.pressureHighClients = []
        self.checkPressureEvent = Event(name='''%s Check Pressure''' % (self._name))
        self.checkMaxEvent = Event(name='''%s Check Max Pressure''' % (self._name))
        self.calibrateSensorEvent = Event(name='''%s Calibrate Sensor''' % (self._name))
        self.calibrateValidate = cv
        self._validCommandlist = []
        self._valveMonitorEvents = []
        self.registerMonitorEvent('checkPressure', self.checkPressureEvent, self.checkPressure)
        self.registerMonitorEvent('checkMax', self.checkMaxEvent, self.checkMax)
        self.registerMonitorEvent('calibrateSensor', self.calibrateSensorEvent, self.calibrateSensor)
        
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

    def convertValue(self, v):
        """ convert value to PSI """
        psi = round((v - 101) * .1708)
        return psi

    def currentPSI(self):
        """read Avg valuse convert to psi and set self.PSI and event data"""
        self.avgRaw = self.avgread()
        self.psi = self.convertValue(self.avgRaw)
        if self.psi < 0:
            self.psi = 0
        return self.psi

    def name(self):
        return self._name
    
    def readPressure(self):
        msg = 'not read'
        psi = self.currentPSI()
        if psi>self.maxPsi:
            self.maxPsi = psi
        if psi<self.cutoffPressure:
            self.pressureHighEvent.clear()
        if psi>self.lowPressure:
            self.pressureLowEvent.clear()
        if psi<self.lowPressure and self.lastPSI!=psi:
            self.pressureLowEvent.set(psi)            
            msg = """Low Pressure warning: %s""" % (psi)
        elif psi>self.highPressure and psi<self.cutoffPressure:
            msg = """High Pressure warning: %s""" % (psi)            
        elif psi>self.cutoffPressure:
            self.pressuerHighEvent.set(psi)
            msg = """Dangerous Pressure: %s, Shut Down Pump!!!""" % (psi)
        else:
            msg = """%s reading: %s""" % (self.name, psi)
        self.lastPSI = psi            
        return msg

    def registerCalibrateSensorEvent(self, event):
        return self.calibrateSensorEvent
    
    def registerCheckPressure(self):
        return self.checkPressureEvent

    def registerCheckMax(self, event):
        return self.checkMaxEvent
    
    def registerMonitorEvent(self, name, event, func):
        self._validCommandlist.append(validCommand(Name, event))
        self._valveMonitorEvents.append((Event, func))

    def registerPressureHigh(self, event):
        self.pressureHighClients.append(event)
        return self.pressureHighEvent
    
    def registerPressuerLow(self, event):
        self.pressureLowClients.append(event)
        return self.pressureLowEvent
    
    def registerRunning(self, event):
        self.runningEvent = event
        return 1    

    def validCommandList(self):
        return self._validCommandList

    async def calibrateSensor(self):        
        if self.runningEvent():# and self.calibrateValidate()==cv:
            self.sensorLowCorrection = round(self.avgread())
            self.calibrateSensorEvent.value().set("""sensorLowCorrection set to %s""" % (self.sensorLowCorrection))
        print(event.value())

    async def checkPressure(self, debug=True):
        self.presureCheckEvent.value().set(self.readPressure())
        if debug:
            print("""checkPressure msg: %s """ % (self.presureCheckEvent.value().value()))
    
    async def monitorPressure(self, event=False):
        print('''%s - %s: Monitor of pressure sensor started''' % (self._name, time.time()))
        while True:
            await asyncio.ms_sleep(50)
            self.readPressure()
            for event, func in self._valveMonitorEvents:
                await asyncio.ms_sleep(50)
                if event.is_set():
                    mainLoop = asyncio.get_event_loop()
                    mainLoop.create_task(func(event.value()))
                    print('''%s - %s: event %s set, adding func %s to loop''' % (self._name, time(), event.name(), func))
                    event.clear()                
              