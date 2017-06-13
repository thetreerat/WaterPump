# Author: Harold Clark
# Copyright Harold Clark 2017
#
class validCommand(object):
    def __init__(self,name='',event=None,commandArgs={}):
        self._name = name
        self.event = event
        self.commandArgs = commandArgs
    
    def name(self):
        return self._name
    
    def printCommand(self):
        print(self._name)