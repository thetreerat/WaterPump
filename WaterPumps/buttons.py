# Author: Harold Clark
# Copyright Harold Clark 2017
#

try:
    import lib.uasyncio as asyncio
except ImportError:
    import uasyncio as asyncio
from utime import time
from WaterPumps.events import Event

class button(object):
    debounce_ms = 50
    def __init__(self, pin, state=None, name='Test'):
        """ init a button  object"""
        import machine
        from WaterPumps.buttons import states 
        #from WaterPumps.server_uasyncio import Event
        self.pin = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP)
        self.states = states()
        if state==None:
            self.state = self.states.nextState()
        else:
            self.state = state
        self.buttonState = False
        self._name = name
        
        
        
    def addTasktoLoop(self, func, args):
        """add a func to main loop"""
        import uasyncio as asyncio
        buttonTask = func(self.event)
        mainLoop = asyncio.get_event_loop()
        mainLoop.create_task(buttonTask)
        
    async def monitorButton(self, startState='pumpOff', debug=True):
        """async coroutine for check state of multiple state buttons"""
        #self.state = self.setCurrentState(startState)
        print('''%s - %s: Monitor button start in state: %s''' % (self._name, time(),self.state.state))
        pumpMessage = Event()
        while True:
            if not self.pin.value():
                #if debug:
                #    print("Button Pressed currently!!")
                if not self.buttonState:
                    if debug:
                        print('''Button state changed from %s''' % (self.state.state))
                    self.state = self.states.nextState()
                    if not self.state.event.is_set():
                        self.state.event.set(pumpMessage)
                        if debug:
                            print('''Button State changed to %s''' % (self.state.state))
                    else:
                        print("""%s - %s: event was active, nothing will be done""" % (self._name, time()))
                    if self.state.event.is_set():
                        #self.addTaskLoop(self.state.func, self.state.args)
                        print('''%s - %s: Event is live''' % (self._name, time()))
                    self.buttonState = True                    
            else:
                self.buttonState = False
            if pumpMessage.is_set():
                print(pumpMessage.value)
                pumpMessage.clear()
            await asyncio.sleep_ms(button.debounce_ms)            
                                
    def setCurrentState(self, state):
        while self.state!=state:
            self.state = self.states.nextState()
            
class states(object):
    """class for multiple state, not finished"""
    def __init__(self, states=False):
        """inilize states"""
        from WaterPumps.buttons import state
        if states:
            self.states = states
        else:
            self.states = [state('Fasle'),state('True')]
        
    def nextState(self):
        """Toggle state"""
        state = self.states.pop()
        self.states.insert(0,state)
        return state
    
    
    def setStates(self, newStateList):
        """redefine state list"""
        self.states = newStateList

class state(object):
    """class for a valid state"""
    def __init__(self,state,event=None,args=False):
        """Inilize class object"""
        self.state = state
        self.event = event
        if not args:
            self.args = args
        else:
            self.args = []