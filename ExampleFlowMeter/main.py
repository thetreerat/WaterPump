# Author: Harold Clark
# Copyright Harold Clark 2017
#
import uasyncio as asyncio
from WaterPumps.flowMeters import flowMeter
import logging

logging.basicConfig(level=logging.DEBUG)
mainFlowMeter = flowMeter(flowPin=4, rate=4.8)

flowCount = 0

def callbackflow(p):
    """Add on to Counter """
    global flowCount
    flowCount += 1
    print("""callback count: %s""" % (flowCount))

#register callback for flowmeter
mainFlowMeter.counterPin.irq(trigger=mainFlowMeter.counterPin.IRQ_RISING, handler=callbackflow)

#Get handle for event loop
main_loop = asyncio.get_event_loop()

#load flow monitor task
main_loop.create_task(mainFlowMeter.monitorFlowMeter())

#start main loop
main_loop.run_forever()
main_loop.close()