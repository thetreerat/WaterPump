import network
import time
import socket
import sys

class pumpServer(object):
    def __init__(self, pump, port=8888, host='', connectionCount=5, serverObjects=None):
        """init pump server"""
        self.port = port
        self.host = host
        self.connectionCount = connectionCount
        self.socket = None
        self.pumpServerStart()
        self.serverObjects = [{'objectID':'mainPump', 'object':pump},{'objectID':'Test', 'object':pump}]
        #if serverObjects==None:
        #    self.serverObjects = []
        #else:
        #    self.serverObjects = serverObjects


    def pumpServerStart(self):  
        """Server for pump objects"""
        # self.HOST  - Symbolic name meaning all available interfaces
        # self.PORT - Arbitrary non-privileged port
 
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket created')
 
        self.socket.bind((self.host, self.port))
         
        print('Socket bind complete')
     
        self.socket.listen(self.connectionCount)
        print('Socket now listening')
        
    def listenForConnection(self):
        #wait to accept a connection - blocking call
        c = pumpconnection(self.serverObjects)
        while 1:
            c.conn, c.addr = self.socket.accept()     
            print("""Connected with %s:%s""" % (c.addr[0], str(c.addr[1])))
     
            #now keep talking with the client
            c.cleanData = str(c.conn.recv(512))
            if not c.data or c.cleanData=='exit':
                break        
            conn.sendall(c.message)
            print(c.message)
            cconn.close()
        self.socket.close()
        
        
class pumpconnection(object):
    """Object for holding connection data"""
    def __init__(self, serverObjects):
        """init object with conn, addr"""
        self.conn = None
        self.addr = None 
        self.data = None
        self.cleanData = None
        self.message = None
        self.objectID = None
        self.serverObjects = serverObjects
    
    def clean(self, data):
        """Cleaned data from client"""
        self.cleanData =  str(data)[2:-5]
        #colon = instr(cleanData)
        self.objectID = 'mainPump'
        self.cleanData = str(cleanData)
        self.checkMessage()
    
    def NewData(self, data):
        """add data, and cleandata to object"""
        self.data = data
        self.clean()
    
    
    def checkMessage(self, debug=False):
        if self.cleanData=='exit':
            self.message = 'exit'
        elif not self.objectID==None:
            for l in self.serverObjects:
                if l['objectID']=='Test':
                    self.message = l['object'].serverRequest('bob')
            self.serverObjects['MainPump']
        else:
            if debug:
                print(self.cleanData)
            self.message = 'exit'
        self.message = """%s/n""" % (self.message)    
    

    def holdstuff(self):
        if cleandata=='pump_status':
            status = pumpStatus()
        elif cleandata=='pump_on':
            if not pumpPower.value():
                changePumpPower()    
                status = 'starting pump ...\n'
            else:
                status = 'pump is already on!\n'
        elif cleandata=='pump_off':
            if pumpPower.value():
                changePumpPower()
                status = "shuting down pump ...\n"
            else:
                status = "pump was already off!\n"
