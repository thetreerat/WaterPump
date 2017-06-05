# Author: Harold Clark
# Copyright Harold Clark 2017
#
try:
    import lib.uasyncio.core as asyncio
except ImportError:
    import uasyncio.core as asyncio
from WaterPumps.events import Event
from utime import time

class pumpServer(object):
    """Class for pumpserver using uasyncio"""
    def __init__(self, host='', port=8888, name='Test Server'):
        """initilzed the pump server class """
        import machine
        self._name = name
        self.host = host
        self.port = port
        self.validCommands = []
        
    def name(self):
        return self._name
    
    
    def validCommandList(self):
        """Method for extrating list for vaild commands"""
        list = []
        for v in self.validCommands:
            list.append(v.name())
        return list    
            
    def clearvalidCommandList(self):
        """Clear the CommandList to prep for reload of list"""
        self.validCommands = []
    
    
    def appendvalidCommandlist(self, commands):
        """Add new memebers the validCommandList """
        if type(commands) is list:
            for i in commands:        
                self.validCommands.append(i)
        else:
            self.validCommands.append(commands)
    
    def setvalidCommandList(self, commands):
        """Set validCommandlist to list of supplied commands"""
        self.clearvalidCommandList()
        self.appendvalidCommandlist(commands)
                
    def addTasktoLoop(self, command, event, debug=True):
        """add a func to main loop"""
        msg = "bad no coro"
        for c in self.validCommands:
            if c.name==command:        
                pservertask = c.commandCoro(event)
                mainLoop = asyncio.get_event_loop()
                if debug:
                    print("""Loaded task: %s as handle %s""" % (c.name, pservertask))
                mainLoop.create_task(pservertask)
                msg = c.commandCoro
                return msg                
        return msg
    
    
    def pserverHelp(self):
        msg = """Welcome to %s\n\r\n\rip: %s on port %s\n\rexit - Exit session\n\rlist - list avalible commands\n\r
help - this info\n\r""" % (self._name,
                        self.host,
                        self.port)
        return msg
    
    
    def pserverList(self):
        msg = """List of commands\n\r"""
        for c in self.validCommandList():
            msg = '''%s%s\n\r''' % (msg,c) 
        return msg
    
    def telnetPrint(self, msg):
        """function for converting message from moduole to telnet happy strings"""
        msg = """%s\n\r""" % (msg)
        return msg
    
    def getEvent(self, commandName):
        for ValidCommand in self.validCommands:
            if ValidCommand.name()==commandName:
                return ValidCommand.event
    @asyncio.coroutine
    def pserver(self, reader, writer):
        """coroutine for reading server requests"""
        print(reader, writer)
        print("================")
        CommandDataEvent = Event()
        while True:
            command = yield from reader.read()
            command = str(command)[2:-5]
            msg = ''
            if command in self.validCommandList():
                event = self.getEvent(command)
                event.set(CommandDataEvent)
                print('''%s - %s: server request %s'''%(event._name, time(),event.value()._name))
                await CommandDataEvent
                msg = self.telnetPrint(CommandDataEvent.value())
                CommandDataEvent.clear()
                
            elif command=='help':
                msg = self.pserverHelp()
            elif command=='list':
                msg = self.pserverList()
            elif command in ['exit','quit']:
                msg = "bye\n\r"
            else:
                msg = """Invalid Code - %s\n\r""" % (command)
            print(msg)
            yield from writer.awrite(msg)
            print("After response write")
            if command in ['exit', 'quit']:
                break
        yield from writer.aclose()
        print("Finished processing request")  
    


