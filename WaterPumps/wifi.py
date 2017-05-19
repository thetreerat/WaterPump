import network
import time
import webrepl
class wifiHelper(object):
    """Class for connecting to wifi netowrks and starting the Webrepl"""
    def __init__(self, sid='lakenet', password='password'):
        """wifi helper inilize"""
        self.sta_if = network.WLAN(network.STA_IF)
        self.sid = sid
        self.password = password
        self.sta_ip = None
        self.sta_mask = None
        self.sta_router = None
        self.sta_DNS = None
    
    
    def connectWifi(self):
        """connect wifi on self.sid, and self.password"""
        if not self.sta_if.isconnected():
            print('connecting to network...')
            self.sta_if.active(True)
            self.sta_if.connect(self.sid, self.password)
            time.sleep(5)
        self.loadIP()
        print('''network config:\r\nIP: %s\r\nMask: %s, Router: %s, DNS: %s''' % (self.sta_ip, self.sta_mask, self.sta_router, self.sta_DNS))
        
    def loadIP(self):
        self.sta_ip,self.sta_mask,self.sta_router,self.sta_DNS = self.sta_if.ifconfig()
        
    def startAP(self):
        """Start the access point"""
        pass    