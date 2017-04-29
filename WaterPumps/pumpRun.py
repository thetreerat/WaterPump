# Author: Harold Clark
# Copyright Harold Clark 2017
#

class pumpRun(object):
    def __init__(self):
        import time
        self.start = time.time()
        self.finish = False
        self.maxPSI = False
        self.pumpedTotal = False
    
    
    def pumpOff(self):
        import time
        self.finish = time.time()
        
        
    def totalRunTime(self):
        if self.finish:
            totalRunTime = time.time() - self.start 
        else:
            totalRunTime = self.finish - self.start
        return totalRunTime
        
