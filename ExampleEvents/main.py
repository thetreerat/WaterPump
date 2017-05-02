# Author: Harold Clark
# Copyright Harold Clark 2017
#
import uasyncio as asyncio
from WaterPumps.flowMeters import flowMeter
from WaterPumps.flowMeters import callbackflow
from WaterPumps.pumps import pump
from WaterPumps.leds import triLed
from WaterPumps.buttons import button
import logging


logging.basicConfig(level=logging.DEBUG)
#mainFlowMeter = flowMeter(flowPin=4, rate=4.8)

#inialize led
statusLed = triLed(redpin=13,bluepin=15,greenpin=12, name='statusLED')
#make led yellow while booting program
statusLed.makeYellow()

#inialize Pump objects: buttons, leds,flowsensors,pressure sensors, server process
mainPump = pump(powerPin=14)
powerButton = button(5,state=False)


#statusLed.registerLedClient(([(mainPump.pumpStartEvent.value, time.time)],statusLed.makeOrange,None,0))
statusLed.registerLedClient(([(mainPump.pumpNotReadyEvent.is_set, True)],statusLed.makeYellow,None),0)
statusLed.registerLedClient((([(mainPump.pumpNotReadyEvent.is_set, False), (mainPump.pumpRunningEvent.is_set, True)]),statusLed.makeGreen,None),1)
statusLed.registerLedClient(([(mainPump.pumpNotReadyEvent.is_set, False), (mainPump.pumpRunningEvent.is_set, False)],statusLed.makeBlue,None),2)
mainPump.registerPumpServer(statusLed.name())
#register callback for flowmeter
#mainFlowMeter.counterPin.irq(trigger=mainFlowMeter.counterPin.IRQ_RISING, handler=callbackflow)

#Get handle for event loop
main_loop = asyncio.get_event_loop()

#load flow monitor task
#main_loop.create_task(mainFlowMeter.monitorFlowMeter())
main_loop.create_task(mainPump.monitorPump())
main_loop.create_task(statusLed.monitorLED())
main_loop.create_task(powerButton.monitorButton())
#start main loop
mainPump.pumpNotReadyEvent.clear()
main_loop.run_forever()
main_loop.close()