# Author: Harold Clark
# Copyright Harold Clark 2017
#
class validCommand(object):
    """Class for a Vaild Command on server"""
    def __init__(self,name='',event=None,commandArgs=None):
        """initilized vaildCommand"""
        self._name = name
        self.event = event
        self.commandArgs = commandArgs
    
    def name(self):
        return self._name
    
    def printCommand(self):
        print(self._name)