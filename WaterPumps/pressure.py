import machine
import time

class pressureSensor(object):
    """ Class for pressure sensor """
    def __init__(self, pin=0):
        """ init a Pressure sensor """
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


    def CheckPressure(self, pump, statusLED):
        """check values and print warning if needed"""
        psi = self.currentPSI()
        if psi<self.lowPressure and self.lastPSI!=psi:
            print("""Low Pressure warning: %s""" % (psi))
        elif psi>self.highPressure and psi<self.cutoffPressure:
            print("""High Pressure warning: %s""" % (psi))
        elif psi>self.cutoffPressure:
            print("""Danguras Pressure Warning, Shut Down Pump!!!""")
            if pump!=None:
                pump.pumpOff(self.LED)
                statusLED.makeRed()
        self.lastPSI = psi
            
    
    def convertValue(self, v):
        """ convert value to PSI """
        psi = round((v - 101) * .1708)
        return psi