# Author: Harold Clark
# Copyright Harold Clark 2017
#
from WaterPumps.flowMeters import flowMeter
from WaterPumps.flowMeters import callbackflow
from WaterPumps.pumps import pump
from WaterPumps.leds import triLed
from WaterPumps.buttons import button
from WaterPumps.buttons import state
#from WaterPumps.servers import pumpServer
#from WaterPumps.servers import validCommand
try:
    import lib.uasyncio as asyncio
except ImportError:
    import uasyncio as asyncio
try:
    import lib.logging as logging
except ImportError:
    import logging

logging.basicConfig(level=logging.DEBUG)



#inialize led
statusLed = triLed(redpin=13,bluepin=15,greenpin=12, name='statusLED')
#make led yellow while booting program
statusLed.setStartColor(statusLed.LED_YELLOW)
#defind button states

#inialize Pump objects: buttons, leds,flowsensors,pressure sensors, server process
mainPump = pump(powerPin=14)
powerButton = button(5, name='Power Button')
mainFlowMeter = flowMeter(flowPin=4, rate=4.8)
#mainServer = pumpServer(host='192.168.1.14')

#inialize button states
states = [state('pumpOff', event=mainPump.pumpOffEvent)]
states.append(state('pumpOn', event=mainPump.pumpOnEvent))
powerButton.states.setStates(states)


#register statusled monitor events
statusLed.registerLedClient(([(mainPump.pumpNotReadyEvent.is_set, True)],statusLed.setColor,statusLed.LED_YELLOW,None),0)
statusLed.registerLedClient((([(mainPump.pumpNotReadyEvent.is_set, False), (mainPump.pumpRunningEvent.is_set, True)]),statusLed.setColor,statusLed.LED_GREEN,None),1)
statusLed.registerLedClient(([(mainPump.pumpNotReadyEvent.is_set, False), (mainPump.pumpRunningEvent.is_set, False)],statusLed.setColor,statusLed.LED_BLUE,None),2)

#register callback for flowmeter
mainFlowMeter.counterPin.irq(trigger=mainFlowMeter.counterPin.IRQ_RISING, handler=callbackflow)

#Get handle for event loop
main_loop = asyncio.get_event_loop()

#register validCommandlists into mainServer
#mainServer.setvalidCommandList(mainPump.validCommandList())
#mainServer.setvalidCommandList(mainFlowMeter.validCommandList())

#load flow monitor task
main_loop.create_task(mainFlowMeter.monitorFlowMeter(debug=False))
main_loop.create_task(mainPump.monitorPump())
main_loop.create_task(statusLed.monitorLED())
main_loop.create_task(powerButton.monitorButton(startState='pumpOff'))
#main_loop.create_task(asyncio.start_server(mainServer.pserver, mainServer.host, mainServer.port))

# register pump events with flow meter
mainFlowMeter.RunningEvent = mainPump.pumpRunningEvent
mainFlowMeter.finishEvent = mainPump.pumpFinishEvent
mainFlowMeter.startupEvent = mainPump.pumpStartEvent
mainFlowMeter.shutoffEvent = mainPump.pumpOffEvent
# register pump run data source
mainPump.registerFinishDataEvent(mainFlowMeter.flowFinishData, 'pumpedTotal')


#finished loading turn led bluw

#start main loop
mainPump.pumpNotReadyEvent.clear()
main_loop.run_forever()
main_loop.close()