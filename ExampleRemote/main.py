# Author: Harold Clark
# Copyright Harold Clark 2017
#

try:
    import lib.uasyncio as asyncio
except ImportError:
    import uasyncio as asyncio
try:
    import logging
except ImportError:
    import lib.logging as logging
from utime import time    

from WaterPumps.buttons import state
from WaterPumps.buttons import button
from WaterPumps.leds import led
from WaterPumps.remotes import remote
from WaterPumps.monitors import monitor
from WaterPumps.controllers import controller
from WaterPumps.events import Event
from remotefunc import pumpOff
from remotefunc import pumpOn


logging.basicConfig(level=logging.DEBUG)



#Get handle for event loop
main_loop = asyncio.get_event_loop()

lakeButton = button(5, name='Lake Button')
parkButton = button(4, name='Park Button')
lakeLed = led(ledPin=12, name='Lake LED')
parkLed = led(ledPin=13, name='Park LED')

#define Events for actions on button press
lakePumpOn = Event(name='Lake Pump On')
lakePumpOff = Event(name='Lake Pump Off')
parkPumpOn = Event(name='Park Pump On')
parkPumpOff = Event(name='Park Pump Off')

#set button states
states = [state('pumpOff', event=lakePumpOff)]
states.append(state('pumpOn', event=lakePumpOn))
lakeButton.states.setStates(states)
states = [state('pumpOff', event=parkPumpOff)]
states.append(state('pumpOn', event=parkPumpOn))
parkButton.states.setStates(states)

#create controller objects
lakePump = controller(ip='192.168.1.9', name='Lake Pump Controller')
parkPump = controller(ip='192.168.1.4', name='Park Pump Controller')

remote = remote(name='Remote Control')
remote.registerMonitor(monitor(name='Park Pump On', event=parkPumpOn, func=pumpOn, args=(parkPump.ip,parkLed,parkPumpOn)))
remote.registerMonitor(monitor(name='Park Pump Off', event=parkPumpOff, func=pumpOff, args=(parkPump.ip,parkLed,parkPumpOff)))
remote.registerMonitor(monitor(name='Lake Pump On', event=lakePumpOn, func=pumpOn, args=(lakePump.ip,lakeLed,lakePumpOn)))
remote.registerMonitor(monitor(name='Lake Pump Off', event=lakePumpOff, func=pumpOff, args=(lakePump.ip,lakeLed,lakePumpOff)))

#create task
main_loop.create_task(lakeButton.monitorButton(startState='pumpOff',debug=False))
main_loop.create_task(parkButton.monitorButton(startState='pumpOff',debug=False))
main_loop.create_task(lakeLed.monitorLED())
main_loop.create_task(parkLed.monitorLED())
main_loop.create_task(remote.monitorRemote())

#start main loop
main_loop.run_forever()
main_loop.close()