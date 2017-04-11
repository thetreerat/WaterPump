import machine
import time
import os
import network
import webrepl

from WaterPumps.pumps import pump
from WaterPumps.flowMeters import flowMeter
from WaterPumps.buttons import button
from WaterPumps.leds import triLed
from WaterPumps.servers import pumpServer
from WaterPumps.pressure import pressureSensor


changeButton = False
flowCount = 0
                        
powerButton = button(machine.Pin(5, machine.Pin.IN, machine.Pin.PULL_UP))            
mainFlowMeter = flowMeter(flowPin=4, rate=4.8)
mainPump = pump(powerPin=14)
statusLed = triLed(redpin=13,bluepin=15,greenpin=12)
pumpServer = pumpServer(port=8888, host='', connectionCount=5)
pumpServer.setvalidCommandList(commands=mainPump.validCommandList())
mainPressure = pressureSensor(pin=0)

def callbackButton(p):
        """Change button state on button push"""
        global changeButton
        changeButton = True

def callbackflow(p):
    """Add on to Counter """
    #print("count")
    global flowCount
    flowCount += 1
    #print("""flowcount""")
    #print(flowCount)
loopCount = 0


def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('lakenet', 'keem34&2')
        time.sleep(5)
    print('network config:', sta_if.ifconfig())
    if sta_if.isconnected():
        webrepl.start()
        return True
    else:
        #ap_if = network.WLAN(network.AP_IF)
        #print('Starting AP ...')
        #ap_if.active(True)
        #time.sleep(2)    
        #if ap_if.isconnected():
        #    webrepl.start()
        #    return True
        #else:
        return False
        
powerButton.pin.irq(trigger=powerButton.pin.IRQ_RISING, handler=callbackButton)
mainFlowMeter.counterPin.irq(trigger=mainFlowMeter.counterPin.IRQ_RISING, handler=callbackflow)

def clearMain():
    os.remove('main.py')

do_connect()    
statusLed.makeBlue()    
while True:
        bstate = None
        time.sleep(.1)
        #pbIRQstate = machine.irq_disable()
        #servermsg = pumpServer.listenForConnection()
        
        if changeButton==True:
            changeButton=False
            if powerButton.state==True:
                print("Turning off Power")
                bstate = False
                mainPump.pumpOff(statusLed)
                flowCount = 0
            else:
                print("Turing Power on")
                bstate = True
                mainPump.pumpOn(statusLed)
            powerButton.state = bstate
        if mainPump.Power.value() and mainPump.timeOn() > mainPump.startupTime and flowCount==0:
            mainPump.pumpOff(statusLed)
            powerButton.state = False
        #else:
        #    print("""TimeOn :%s""" % (mainPump.calculateTimeOn()))  

        if flowCount>0:
            mainPump.flow = True
            statusLed.makeGreen()
            #print('main loop, flowCount > 0')
            if mainFlowMeter.currentTime<int(time.time()):
                mainFlowMeter.setFlowCount(flowCount)
                flowCount = 0            
                Hz = mainFlowMeter.calculateflow(debug=False)
                totalseconds = time.time() - mainFlowMeter.flowStartTime
                totalliters = mainFlowMeter.totalFlowCount/450
                print("""Current Flow (L/M): %s""" % (mainFlowMeter.flowRate))
                print("""Total Liters: %s""" % (totalliters))
        if mainPump.Power.value()==True and mainPump.timeOn() > mainPump.startupTime:
                mainPressure.CheckPressure(mainPump,statusLed)
        loopCount += 1