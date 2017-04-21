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
import logging
from install_waterpump import waterpumpinstall
#from WaterPumps.servers import pumpServer
#from WaterPumps.servers import pumpconnection

import machine
import time
import os

@asyncio.coroutine
def pserver(reader, writer, args=[]):
    """coroutine for reading server requests"""
    print(reader, writer)
    print("================")
    while True:
        command = yield from reader.read()
        validCommandList = args['validCommandList']
        print(command)
        command = str(command)[2:-5]
        msg = ''
        if command in validCommandList:
            msg = "Hit\n\r"
        elif command=='exit':
            msg = "bye\n\r"
        else:
            msg = "Invalid Code\n\r"
        print(msg)
        yield from writer.awrite(msg)
        print("After response write")
        if command=='exit':
            break
    yield from writer.aclose()
    print("Finished processing request")  


#helper for cleaning and moving waterpump modules
i = waterpumpinstall

#set logging level, options: CRITICAL,ERROR,WARNING,INFO,DEBUG - listed least to most
logging.basicConfig(level=logging.DEBUG)

#Get handle ofr event loop
main_loop = asyncio.get_event_loop()

#inialize Pump objects: buttons, leds,flowsensors,pressure sensors, server process
mainPump = pump(powerPin=14)
statusLed = triLed(redpin=13,bluepin=15,greenpin=12)
powerButton = button(5,state=False)
mainServer = pumpServer(host='192.168.1.14')
mainpressure = pressureSensor(0,20,150,170)

#start the pump server process
#mainServer.pumpServerStart()

#load functions into button action methods
powerButton.onFunc(mainPump.pumpOn,[statusLed])
powerButton.offFunc(mainPump.pumpOff,[statusLed])

#register validCommandlists into mainServer
mainServer.setvalidCommandList(mainPump.validCommandList())


#Load buttons,pressures,server in to Loop
args = {'validCommandList':mainServer.validCommandList}
main_loop.create_task(mainpressure.CheckPressure(mainPump,statusLed))
main_loop.create_task(powerButton.checkButton())
main_loop.create_task(asyncio.start_server(pserver, mainServer.host, mainServer.port, args))

#main_loop.create_task(mainServer.listenForConnection())

#start main loop
main_loop.run_forever()
main_loop.close()