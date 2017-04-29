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


#import uasyncio.core as asyncio
import uasyncio as asyncio
from WaterPumps.pumps import pump
from WaterPumps.leds import triLed
from WaterPumps.pressure import pressureSensor
from WaterPumps.buttons import button
from WaterPumps.server_uasyncio import pumpServer
from WaterPumps.server_uasyncio import validCommand
from WaterPumps.flowMeters import flowMeter

import logging
import machine
import time
import os


#set logging level, options: CRITICAL,ERROR,WARNING,INFO,DEBUG - listed least to most
logging.basicConfig(level=logging.DEBUG)


#inialize Pump objects: buttons, leds,flowsensors,pressure sensors, server process
statusLed = triLed(redpin=13,bluepin=15,greenpin=12)
mainPump = pump(powerPin=14)
powerButton = button(5,state=False)
mainServer = pumpServer(host='192.168.1.14')
mainpressure = pressureSensor(0,20,150,170)
mainFlowMeter = flowMeter(flowPin=4, rate=4.8)

flowCount = 0

def callbackflow(p):
    """Add on to Counter """
    global flowCount
    flowCount += 1
    print("""callback count: %s""" % (flowCount))


#helper for cleaning and moving waterpump modules
#i = waterpumpinstall

#add mainPump, statusLED object pointer to pressuresensor
mainpressure.pump = mainPump
mainpressure.statusLED = statusLed

#load functions into button action methods
powerButton.onFunc(mainPump.pumpOn,[statusLed])
powerButton.offFunc(mainPump.pumpOff,[statusLed])

#register validCommandlists into mainServer
mainServer.setvalidCommandList(mainPump.validCommandList())
mainServer.appendvalidCommandlist(mainpressure.validCommandList())

#register callback for flowmeter
mainFlowMeter.counterPin.irq(trigger=mainFlowMeter.counterPin.IRQ_RISING, handler=callbackflow)

#Get handle for event loop
main_loop = asyncio.get_event_loop()

#Load buttons,pressures,server in to Loop
main_loop.create_task(mainFlowMeter.monitorFlowMeter())
main_loop.create_task(mainpressure.MonitorPressure())
main_loop.create_task(powerButton.checkButton())
main_loop.create_task(asyncio.start_server(mainServer.pserver, mainServer.host, mainServer.port))

#main_loop.create_task(mainServer.listenForConnection())

#start main loop
main_loop.run_forever()
main_loop.close()