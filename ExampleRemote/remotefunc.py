# Author: Harold Clark
# Copyright Harold Clark 2017
#
try:
    import lib.uasyncio as asyncio
except ImportError:
    import uasyncio as asyncio
from utime import time    
from WaterPumps.events import Event

async def pumpOn(controller,led,event):
    pumpOnEvent = Event(name='pumpOn return message')
    controller.addMessage(command='pumpOn\r\n', pumpOnEvent)
    await pumpOnEvent
    if pumpOnEvent.value() == 'Pump Turned On':
        led.ledOnEvent.set()
    else:
        led.ledOffEvent.set()
    print('''%s - %s: pump msg(%s): %s''' % (pumpIP, time(),len(pumpmsg),pumpmsg))    
    event.clear()
    
    
async def pumpOff(controller,led,event):
    pumpOffEvent = Event(name='pumpOffEvent return message')
    controller.addMessage(commmand='pumpOff\r\n', pumpOffEvent)
    await pumpOffEvent
    if not pumpOffEvent.value() in ('Pump Turned off','Pump was already off!'):
        print('''error: %s''' % (pumpOffEvent.value()))
    print('''%s - %s: pump msg: %s''' % (controller.name(), time(),pumpoffEvent.value()))
    led.ledOffEvent.set()
    event.clear()
    
async def checkPump(controller, led):
    checkPumpEvent = Event(name='checkPumpEvent')
    while True:
        asyncio.sleep(2)
        controller.addMessage(command='pumpStatus\r\n',checkPumpEvent)
        await checkPumpEvent
        if checkPumpEvent.value()[:10]=='Pump is on':
            led.ledOnEvent.set()
        print('''%s - %s: msg: %s''' % (controller.name(),time(),checkPumpEvent.value()))
        checkPumpEvent.clear()
        