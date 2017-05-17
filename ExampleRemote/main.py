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

powerButton = button(5, name='Power Button')
statusLed = triLed(redpin=13,bluepin=15,greenpin=12, name='statusLED')
upButton = button(4, name='Up Button')
downButton = button(14, name='Down Button')

#set button states
states = [state('pumpOff', event=Event())]
states.append(state('pumpOn', event=Event())
powerButton.states.setStates(states)
states = [state('up', event=Event())]
upButton.states.setStates(states)
states = [state('down', event=Event())]
upButton.states.setStates(states)

#Get handle for event loop
main_loop = asyncio.get_event_loop()

#Load tasks
main_loop.create_task(powerButton.monitorButton(startState='pumpOff',debug=False))

#start main Loop
main_loop.run_forever()
main_loop.close()