# Author: Harold Clark
# Copyright Harold Clark 2017
#

class monitor(object):
    def __init__(self,name, event, func, args=()):
        self._name = name
        self.event = event
        self.func = func
        self.args = args
    
    def name(self):
        return self._name