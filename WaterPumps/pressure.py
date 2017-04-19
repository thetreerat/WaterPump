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
        self.pressure = machine.ADC(pin)
        self.avgRaw = self.avgread()
        self.psi = self.convertValue(self.avgRaw)
        self.lowPressure = 20
        self.highPressure = 150
        self.cutoffPressure = 170
        self.sensorLowCorrection = 101
        self.ADCPressureConstence = .1708
        self.lastPSI = 0
    

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
    
    def currentPSI(self):
        """read Avg valuse convert to psi and set self.PSI"""
        self.avgRaw = self.avgread()
        self.psi = self.convertValue(self.avgRaw)
        if self.psi < 0:
            self.psi = 0
        return self.psi


    async def CheckPressure(self, pump, statusLED):
        """check values and print warning if needed"""
        while True:
            psi = self.currentPSI()
            if psi<self.lowPressure and self.lastPSI!=psi:
                print("""Low Pressure warning: %s""" % (psi))
            elif psi>self.highPressure and psi<self.cutoffPressure:
                print("""High Pressure warning: %s""" % (psi))
            elif psi>self.cutoffPressure:
                print("""Danguras Pressure Warning, Shut Down Pump!!!""")
                pump.pumpOff(statusLED)
            self.lastPSI = psi
            print(self.lastPSI)
            await asyncio.sleep(4)
    
    def convertValue(self, v):
        """ convert value to PSI """
        psi = round((v - 101) * .1708)
        return psi
    
    def CalibrateSensor(self):
        """This sets the sensorLowCorrection value, this should only be run when there is
           no pressure on the sensor as it will adjust what is a 0 psi reading"""
        self.sensorLowCorrection = round(self.avgread())
        print("""sensorLowCorrection set to %s""" % (self.sensorLowCorrection))
        