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
        self.pumpMessage = Event(name='Button Data Return Event')
        
        
        
    def addTasktoLoop(self, func, args):
        """add a func to main loop"""
        import uasyncio as asyncio
        buttonTask = func(self.event)
        mainLoop = asyncio.get_event_loop()
        mainLoop.create_task(buttonTask)
        
    async def monitorButton(self, startState='pumpOff', debug=True):
        """async coroutine for check state of multiple state buttons"""
        self.setCurrentState(startState)
        print('''%s - %s: Monitor button start in state: %s''' % (self._name, time(), self.state.name))
        self.pumpMessage.clear()
        while True:
            if not self.pin.value():
                #if debug:
                #    print("Button Pressed currently!!")
                if not self.buttonState:
                    if debug:
                        print('''Button state changed from %s''' % (self.state.name))
                    self.state = self.states.nextState()
                    if not self.state.event.is_set():
                        self.state.event.set(self.pumpMessage)
                        if debug:
                            print('''Button State changed to %s''' % (self.state.name))
                    else:
                        print("""%s - %s: event was active, nothing will be done""" % (self._name, time()))
                    if self.state.event.is_set():
                        #self.addTaskLoop(self.state.func, self.state.args)
                        print('''%s - %s: Event is live''' % (self._name, time()))
                    self.buttonState = True                    
            else:
                self.buttonState = False
            if self.pumpMessage.is_set():
                print(self.pumpMessage.value)
                self.pumpMessage.clear()
            await asyncio.sleep_ms(button.debounce_ms)            
                                
    def setCurrentState(self, stateName):
        StateObject = self.states.initState(stateName)
        self.state = StateObject
            
class states(object):
    """class for multiple state, not finished"""
    def __init__(self, states=False):
        """inilize states"""
        from WaterPumps.buttons import state
        if states:
            self.values = states
        else:
            self.values = [state('False'),state('True')]
        
    def nextState(self):
        """Toggle state"""
        state = self.values.pop()
        self.values.insert(0,state)
        return state
    
    
    def setStates(self, newStateList):
        """redefine state list"""
        self.values = newStateList

    def appendStates(self, NewState):
        self.values.append(NewState)
        
    def initState(self, name):
        state = self.nextState()
        while self.values[0].name!=name:
            state = self.nextState()
        return state

class state(object):
    """class for a valid state"""
    def __init__(self,name,event=None,args=False):
        """Inilize class object"""
        self.name = name
        self.event = event
        if not args:
            self.args = args
        else:
            self.args = []