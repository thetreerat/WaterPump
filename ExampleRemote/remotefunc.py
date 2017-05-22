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
    controller.messageQue.insert(0,('pumpOn\r\n',pumpOnEvent))
    await pumpOnEvent
    if pumpOnEvent.value() == 'Pump Turned On':
        led.ledOnEvent.set()
    else:
        led.ledOffEvent.set()
    print('''%s - %s: pump msg: %s''' % (controller.name(), time(),pumpOnEvent.value()))    

        
async def pumpOff(controller,led,event):
    pumpOffEvent = Event(name='pumpOffEvent return message')
    controller.messageQue.insert(0,('pumpOff\r\n', pumpOffEvent))
    await pumpOffEvent
    if not pumpOffEvent.value() in ('Pump Turned off','Pump was already off!'):
        print('''error: %s''' % (pumpOffEvent.value()))
    print('''%s - %s: pump msg: %s''' % (controller.name(), time(),pumpOffEvent.value()))
    led.ledOffEvent.set()
    
    
    
async def checkPump(controller, led):
    checkPumpEvent = Event(name='checkPumpEvent return message')
    while True:
        asyncio.sleep(4)
        controller.messageQue.insert(0,('pumpStatus\r\n', checkPumpEvent))
        await checkPumpEvent
        if checkPumpEvent.value()[:10]=='Pump is on':
            led.ledOnEvent.set()
        elif checkPumpEvent.value()=='Pump is off.':
            led.ledOffEvent.set()
        print('''%s - %s: msg: %s''' % (controller.name(),time(),checkPumpEvent.value()))
        checkPumpEvent.clear()

async def lauchController(controller, event):
    print('''%s - %s: lauchController started''' % (controller.name(), time()))
    await asyncio.sleep(5)
    while controller.notActiveEvent.is_set():
        if controller.notActiveEvent.value() < time(): 
            controller.launchCount += 1
            controller.notActiveEvent.clear()
            main_loop = asyncio.get_event_loop()
            main_loop.create_task(controller.monitorController())
            print('''%s - %s: lauchController add monitor to main loop''' % (controller.name(), time()))
            return
        print('''%s - %s: waiting for launch, sleeping 1 second''' % (controller.name(), time()))
        await asyncio.sleep(1)
            