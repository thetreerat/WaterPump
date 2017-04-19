import machine
import uasyncio.core as asyncio
import time

class button(object):
    debounce_ms = 50
    def __init__(self, pin, state=False):
        """ init a button  object"""
        self.pin = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP)
        self.state = state
        self.buttonState = False
        self._onFunc = False
        self._onArgs = False
        self._offFunc = False
        self._offArgs = False
        
        
    def onFunc(self, func, args=()):
        """Set func for false value of Pin"""
        self._onFunc = func
        self._onArgs = args
    
    
    def offFunc(self, func, args=()):
        """Set func for true value state of button"""
        self._offFunc = func
        self._offArgs = args
        
        
    def addTasktoLoop(self, func, args):
        """add a func to main loop"""
        buttonTask = func(*args)
        mainLoop = asyncio.get_event_loop()
        mainLoop.create_task(buttonTask)
        

    async def checkButton(self, debug=False):
        """async coroutine to check state of button"""
        while True:
            if not self.pin.value():
                if debug==True:
                    print("Button Pressed currently!!")
                if not self.state and not self.buttonState:
                    if debug:
                        print("Button should go on soon!!")
                    self.buttonState=True
                    if self._onFunc:
                        print("Load on func in to main loop")
                        self.addTasktoLoop(self._onFunc,self._onArgs)
                elif self.state and not self.buttonState:
                    self.buttonState=True
                    if debug:
                        print('Button should go off soon!!')
                    if self._offFunc:
                        if debug:
                            print('Load off func in to main loop')
                        self.addTasktoLoop(self._offFunc, self._offArgs)
                self.toggleState()
            else:
                self.buttonState = False
            await asyncio.sleep_ms(button.debounce_ms)
    
    
    def toggleState(self, debug=False):
        """Toggle state"""
        state = None
        if self.state:
            state=False
        else:
            state=True
        self.state = state
        if debug:
            print(state)