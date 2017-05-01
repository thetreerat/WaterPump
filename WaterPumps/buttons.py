# Author: Harold Clark
# Copyright Harold Clark 2017
#
class button(object):
    debounce_ms = 50
    def __init__(self, pin, state=False):
        """ init a button  object"""
        import machine
        #from WaterPumps.server_uasyncio import Event
        self.pin = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP)
        self.state = state
        self.buttonState = False
        self.states = states()
        
        
    def addTasktoLoop(self, func, args):
        """add a func to main loop"""
        import uasyncio as asyncio
        buttonTask = func(self.event)
        mainLoop = asyncio.get_event_loop()
        mainLoop.create_task(buttonTask)
        
    async def checkButton2(self, debug=False):
        """async coroutine for check state of multiple state buttons"""
        import uasyncio as asyncio
        self.state = self.states.nextState()
        while True:
            if not self.pin.value():
                if debug:
                    print("Button Pressed currently!!")
                if not self.buttonState:
                    if debug:
                        print('''Button state changed from %s''' % (self.state.state)):
                    self.state = self.states.nextState()
                    if debug:
                        print('''Button State changed to %s''' % (self.state.state))
                    is self.state.func:
                        self.addTaskLoop(self.state.func, self.state.args)
                    self.buttonState = True                    
            else:
                self.buttonState = False
        await asyncio.sleep_ms(button.debounce_ms)            
                                

class states(object):
    """class for multiple state, not finished"""
    def __init__(self, states=False):
        """inilize states"""
        import state
        if states:
            self.states = [state('Fasle'),state('True')]
        else:
            self.states = states
        
    def nextState(self):
        """Toggle state"""
        state = states.pop()
        states.insert(0,state)
        return state
    
    
    def setStates(self, newStateList):
        """redefine state list"""
        self.states = newStateList

class state(object):
    """class for a valid state"""
    def __init__(self,state,func=None,args=False):
        """Inilize class object"""
        self.state = state
        self.func = func
        if not args:
            self.args = args
        else:
            self.args = []