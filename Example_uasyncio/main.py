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
from WaterPumps.pressure import pressureSensor
from WaterPumps.buttons import button
import machine
import time
import os
def cleanme(name='main.py'):
    if name in os.listdir():
        os.remove(name)
    os.listdir()

def cleanmodule(name):
    module = """WaterPumps/%s""" % (name)
    if name in os.listdir('WaterPumps'):
        os.remove(module)
        print("""removing file %s""" % (module))
    if name in os.listdir():
        os.rename(name,module)
        print("""moved %s to %s""" % (name, module))
    else:
        print("""%s was not found!""" % (name))
    os.listdir()
    
main_loop = asyncio.get_event_loop()
mainPump = pump(powerPin=14)
statusLed = triLed(redpin=13,bluepin=15,greenpin=12)
powerButton = button(5,state=False)

    
async def trueTest(msg):
    """test button add task function"""
    print(msg)
    await asyncio.sleep_ms(50)

mainpressure = pressureSensor(0,20,150,170)

#from WaterPumps.pressure import pressureSensor
#mainPressure = pressureSensor(pin=0)
mainPump.pumpOn(statusLed)
onMsg='Button is now on!'
offMsg='Button is now off'
powerButton.onFunc(mainPump.pumpOn,[statusLed])
powerButton.offFunc(mainPump.pumpOff,[statusLed])
main_loop.create_task(mainpressure.CheckPressure(mainPump,statusLed))
main_loop.create_task(powerButton.checkButton())
main_loop.run_forever()

