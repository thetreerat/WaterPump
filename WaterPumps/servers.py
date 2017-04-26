# Author: Harold Clark
# Copyright Harold Clark 2017
#
import network
import time
import socket
import sys
import uasyncio.core as asyncio

class pumpServer(object):
    def __init__(self, port=8888, host='', connectionCount=5, validCommandList=['PumpOn']):
        """init pump server"""
        self.port = port
        self.host = host
        self.connectionCount = connectionCount
        self.socket = None
        self.validCommandList = validCommandList
        self.ver = '0.9'


    def pumpServerStart(self):  
        """Server for pump objects"""
        # self.HOST  - Symbolic name meaning all available interfaces
        # self.PORT - Arbitrary non-privileged port
 
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket created')
        self.socket.bind(('192.168.1.14',8888))
         
        print('Socket bind complete')
     
        self.socket.listen(self.connectionCount)
        print('Socket now listening')
        
    async def listenForConnection(self):
        #wait to accept a connection - blocking call
        c = pumpconnection(self.validCommandList)
        
        c.conn, c.addr = self.socket.socket.accept()     
        print("""Connected with %s:%s""" % (c.addr[0], str(c.addr[1])))
        await asyncio.sleep_ms(50)
        #now keep talking with the client
        while c.cleanData=='Exit':
            await asyncio.sleep_ms(50)
            c.data = str(c.conn.recv(512))
            c.clean(c.data)
            c.checkMessage(debug=True)        
            c.conn.sendall(c.message)
            print(c.message)
        c.conn.close()
        #self.socket.close()
        await asyncio.sleep_ms(50)
    
    
    def clearvalidCommandList(self):
        """Clear the CommandList to prep for reload of list"""
        self.validCommandList = []
    
    
    def appendvalidCommandlist(self, commands):
        """ Add new memebers the validCommandList """
        if type(commands) is list:
            for i in commands:        
                self.validCommandList.append(i)
        else:
            self.validCommandList.append(commands)
    
    def setvalidCommandList(self, commands):
        """Set validCommandlist to list of supplied commands"""
        self.clearvalidCommandList()
        self.appendvalidCommandlist(commands)
                
        
class pumpconnection(object):
    """Object for holding connection data"""
    def __init__(self, validCommandList):
        """init object with conn, addr"""
        self.conn = None
        self.addr = None 
        self.data = None
        self.cleanData = None
        self.message = None
        self.validCommandList = validCommandList
    
    def clean(self, data):
        """Cleaned data from client"""
        self.cleanData =  str(data)[2:-5]
        #colon = instr(cleanData)
        # not sure about this line HEC
        #self.cleanData = str(self.cleanData)

    
    def NewData(self, data):
        """add data, and cleandata to object"""
        self.data = data
        self.clean()
    
    
    def checkMessage(self, debug=False):
        
        if self.cleanData in self.validCommandList:
            self.message = "Valid command"
        else:
            if debug:
                print("""cleandata: %s        data: %s""" % (self.cleanData,self.data))
                print("""validCommandList count: %s     validCommandList: %s""" % (len(self.validCommandList),self.validCommandList))
            self.message = 'exit'
            self.cleanData = 'exit'
        self.message = """%s\r\n""" % (self.message)    
    

class pumpserverfuture(object):
    def __init__(self):
        self.result = None
        