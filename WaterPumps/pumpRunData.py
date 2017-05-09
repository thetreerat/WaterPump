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
        if not self.finish:
            totalRunTime = time() - self.start 
        else:
            totalRunTime = self.finish - self.start
        return totalRunTime
    
    
    def printRunData(self):
        print("""Run data
              Start Time: %s
              End Time: %s
              Run Time: %s
              Pumped Liters: %s
              MaxPSI: %s""" % (self.start,self.finish, self.totalRunTime(),self.pumpedTotal, self.maxPSI))
        
