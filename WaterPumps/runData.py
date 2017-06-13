# Author: Harold Clark
# Copyright Harold Clark 2017
#
from utime import time
class runData(object):
    def __init__(self, ID=1, Owner='undefined'):
        self.ID = ID
        self.Owner = Owner
        self.start = time()
        self.finish = False
        self.maxPSI = False
        self.totalLiters = False        
        
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
        
