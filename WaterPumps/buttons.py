import machine

class button(object):
    def __init__(self, pin, state=False):
        """ init a button  object"""
        self.state = state
        self.lastState = False
        self.pin = pin


    def toggleState(self, debug=False):
        """Toggle state"""
        state = None
        if self.state():
            state=False
        else:
            state=True
        self.state = state
        if debug:
            print(state)