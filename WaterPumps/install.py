#import os
#import sys
#import time
class waterpumpinstall(object):
    def __init__(self):
        pass
           
    def installNetwork(self):
        import network
        import time
        n = network.WLAN(network.STA_IF)
        n.active(True)
        n.connect('lakenet', 'keem34&2')

    
    def upip_uasync(self):
        from os import listdir        
        upip
        if not 'lib' in os.listdir():
            upip.install('micropython-uasyncio.core')
            
            
    def restart(self, sec=4):
        from utime import sleep
        from machine import reset
        print('''rebooting in %s seconds''' % (sec))
        sleep(sec)
        reset()

if __name__ == "__main__":
    c = waterpumpinstall()
    from network import WLAN
    from network import STA_IF
    n = WLAN(STA_IF)
    if n.active():
        print('renameing main')
        import os
        import sys
        os.rename('main.py', 'install.py')
        os.mkdir('lib')
        os.mkdir('lib/uasyncio')
        #sys.path.append('lib')
        print(os.listdir())
        print(sys.path)
        c.restart(1)
    else:
        print('installing network')
        c.installNetwork()
        c.restart(5)        