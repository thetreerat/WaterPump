# Author: Harold Clark
# Copyright Harold Clark 2017
#

class pumpRunData(object):
    def __init__(self):
        import time
        self.start = time.time()
        self.finish = False
        self.maxPSI = False
        self.pumpedTotal = False        
        
    def totalRunTime(self):
        from utime import time
        if self.finish:
            totalRunTime = time() - self.start 
        else:
            totalRunTime = self.finish - self.start
        return totalRunTime
        
