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
    
from WaterPumps.pressure import pressureSensor

mainpressure = pressureSensor(0,20,150,170)

