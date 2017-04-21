# Author: Harold Clark
# Copyright Harold Clark 2017
#
import machine

class led(object):
    def __init__(self,ledPin=0):
        """Init a single color led object"""
        self.powerPin = machine.Pin(ledPin, machine.Pin.OUT)


class triLed(object):
    def __init__(self, redpin, bluepin, greenpin):
        """Init a Tri color led object"""
        self.redPin = machine.Pin(redpin, machine.Pin.OUT)
        self.bluePin = machine.Pin(bluepin, machine.Pin.OUT)
        self.greenPin = machine.Pin(greenpin, machine.Pin.OUT)
    
    
    def setColor(self, color):
        """set TriColor LED to pass color (RBG)"""
        R, B, G = color
        self.redPin.value(R)
        self.bluePin.value(B)
        self.greenPin.value(G)
        
    def makeGreen(self):
        """Turn Tri Color LED Green"""
        #value(True) = off, vaule(False) = on
        self.redPin.value(True)
        self.greenPin.value(False)
        self.bluePin.value(True)
    
    
    def makeRed(self):
        """ Turn Tri Color LED Red"""
        self.redPin.value(False)
        self.greenPin.value(True)
        self.bluePin.value(True)
        
    
    def makeBlue(self):
        """ Turn Tri Color LED Red"""
        self.redPin.value(True)
        self.greenPin.value(True)
        self.bluePin.value(False)


    def makeYellow(self):
        """ Turn Tri Color LED off"""
        self.redPin.value(False)
        self.greenPin.value(False)
        self.bluePin.value(True)
 
 
    def makeWhite(self):
        """Trun Tri Color LED White"""
        self.redPin.value(False)
        self.greenPin.value(False)
        self.bluePin.value(False)
        
        
    def turnOff(self):
        """ Turn Tri Color LED off"""
        self.redPin.value(True)
        self.greenPin.value(True)
        self.bluePin.value(True)