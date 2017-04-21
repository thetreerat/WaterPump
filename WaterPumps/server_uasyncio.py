# Author: Harold Clark
# Copyright Harold Clark 2017
#
import uasyncio as asyncio

class pumpServer(object):
    """Class for pumpserver using uasyncio"""
    def __init__(self, host='', port=8888):
        """initilzed the pump server class """
        self.host = host
        self.port = port
        self.validCommandList = []


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
                


    @asyncio.coroutine
    def serve(reader, writer):
        """coroutine for reading server requests"""
        print(reader, writer)
        print("================")
        while True:
            print((yield from reader.read()))
            yield from writer.awrite("HTTP/1.0 200 OK\r\n\r\nHello.\r\n")
            print("After response write")
            yield from writer.aclose()
            print("Finished processing request")  
    
