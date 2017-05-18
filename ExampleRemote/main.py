# Author: Harold Clark
# Copyright Harold Clark 2017
#

try:
    import lib.uasyncio as asyncio
except ImportError:
    import uasyncio as asyncio
    
from utime import time
from WaterPumps.events import Event
import socket
import network
from WaterPumps.buttons import button
from WaterPumps.leds import triLed

pins = [4,5,12,13,14,15]

lakeButton = button(5, name='Lake Button')
parkButton = button(4, name='Park Button')
statusLed = triLed(redpin=13,bluepin=15,greenpin=12, name='statusLED')


#set button states
states = [state('pumpOff', event=Event())]
states.append(state('pumpOn', event=Event())
lakeButton.states.setStates(states)
states = [state('pumpOff', event=Event())]
states.append(state('pumpOn', event=Event())
parkButton.states.setStates(states)

#Get handle for event loop
main_loop = asyncio.get_event_loop()

#register led monitors
statusLed.registerLedClient(([(mainPump.pumpNotReadyEvent.is_set, True)],statusLed.setColor,statusLed.LED_YELLOW,None),0)

#Load tasks
main_loop.create_task(powerButton.monitorButton(startState='pumpOff',debug=False))
main_loop.create_task(statusLed.monitorLED())

#start main Loop
main_loop.run_forever()
main_loop.close()