# Author: Harold Clark
# Copyright Harold Clark 2017
#
# Example main.py using uasyncio and coroutines to Impliment WaterPumps
# must load the micropython libary "micropython-uasyncio.core".
# if running a Adafruit Feather HUZZAH with ESP8266 WiFi make sure to alicate more then 8M of the flash
# original how to remcommend a flash_size=8m this is to small for this example use something like this:
#      esptool.py --port /path/to/port --baud 460800 write_flash --flash_size=32m 0 /path/to/image
# you should use at least 1.8.7 release
# with the image up and runing issue:
#      import upip
#      upip.install("micropython_uasyncio.core")  # this fails with 8m of flash size
#
# you also need to copy the folder and all files in /WaterPumps from this project to your board.


import uasyncio.core as asyncio
from WaterPumps.pumps import pump
from WaterPumps.leds import triLed
import machine
import time

main_loop = asyncio.get_event_loop()
mainPump = pump(powerPin=14)
statusLed = triLed(redpin=13,bluepin=15,greenpin=12)

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
                if pump!=None:
                    pump.pumpOff(self.LED)
                    statusLED.makeRed()
            self.lastPSI = psi
            print(self.lastPSI)
            await asyncio.sleep(4)
    
    def convertValue(self, v):
        """ convert value to PSI """
        psi = round((v - 101) * .1708)
        return psi
    
    

statusLed = triLed(redpin=13,bluepin=15,greenpin=12)
mainPump = pump(powerPin=14)
mainpressure = pressureSensor(0,20,150,170)

#from WaterPumps.pressure import pressureSensor
#mainPressure = pressureSensor(pin=0)
main_loop.create_task(mainpressure.CheckPressure(mainPump,statusLed))
main_loop.run_forever()

