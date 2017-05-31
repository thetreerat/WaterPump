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
    
from WaterPumps.valves import valve
from WaterPumps.leds import led
from WaterPumps.buttons import button
from WaterPumps.buttons import state
from WaterPumps.servers import pumpServer
from WaterPumps.validCommands import validCommand

import network
logging.basicConfig(level=logging.DEBUG)
# define valve
pondValve = valve(15, 'Pond Valve')
# define fill button
fillButton = button(5, name='Fill Button')
fillStates = [state('Add 25 gallons', event=valveFunc.AddEvent)]
fillButton.states.setStates(fillStates)
#define cancel Button
cancelButton = button(4, name='Cancel Button')
cancelStates = [state('Cancel fill', event=pondValve.valveOffEvent)]
cancelButton.states.setStates(cancelStates)

#define led
fillLed = led(12, name='Filling led')

