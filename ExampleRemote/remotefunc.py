# Author: Harold Clark
# Copyright Harold Clark 2017
#
try:
    import lib.uasyncio as asyncio
except ImportError:
    import uasyncio as asyncio
    
from WaterPumps.remotes import connectToPump

async def pumpOn(pumpIP,led,event):
    pumpmsg = connectToPump(pumpIP=pumpIP,command='pumpOn\r\n')
    if pumpmsg == 'Pump Turned On\n\r':
        led.ledOnEvent.set()
    else:
        led.ledOffEvent.set()
    event.clear()
    
    
async def pumpOff(pumpIP,led,event):
    pumpmsg = connectToPump(pumpIP=pumpIP,command='pumpOff\r\n')
    if not pumpmsg in ('Pump Turned off\n\r','Pump was already off!\n\r'):
        print('''error: %s''' % (pumpmsg))
    led.ledOffEvent.set()
    event.clear()