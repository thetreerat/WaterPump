import os
import sys
class waterpumpinstall(object):
    def __init__(self):
        pass
    
    def cleanme(name='main.py'):
        """method for cleaning files, default cleans main.py"""
        if name in os.listdir():
            os.remove(name)
        os.listdir()

    def cleanmodule(name):
        """method for clean a module form WaterPumps dir and coping a new one from root"""
        module = """WaterPumps/%s""" % (name)
        if name in os.listdir('WaterPumps'):
            os.remove(module)
            print("""removing file %s""" % (module))
        else:
            print("""%s dose not exist in WaterPumps.""" %(name))
        if name in os.listdir():
            os.rename(name,module)
            print("""moved %s to %s""" % (name, module))
        else:
            print("""%s was not found!""" % (name))
        os.listdir()
        
    def installWaterPumps():
        """method for install or updating waterpumps. copies modules for root to WaterPumps forlder"""
        missingfiles = []
        dirlist = ['lib','WaterPumps']
        for d in dirlist:
            if not d in os.listdir():
                os.mkdir(d)
                print('''Added folder %s''' % (d))
                if not d in sys.path:
                    sys.path.append('WaterPumps')
                    print('''Added %s to path''' % (d))
            else:
                print('''%s exists''' % (d))
        files = ['__init__.py',
                 'core.py']
        copylist(files,'lib/uasyncio/__init__.py')
        
        files = ['pumps.py',
                'servers.py',
                'flowMeters.py',
                'buttons.py',
                'leds.py',
                'wifi.py',
                'server_uasyncio.py',
                'pressure.py']
        copylist(files,'WaterPumps/')

    def copylist(self,files,dest):
        for f in files:
            try:
                os.rename(f, dest + f)
                print('''found %s moved to %s.''' % (f,dest))
            except OSError:
                missingfiles.append(f)
                #print('Error with file %s' % (f))
        if not missingfiles==[]:
            print('files missing: ')
            for f in missingfiles:
                print(f)
    def upip_uasync(self):
        import network
        import upip
        import time
        n = network.WLAN(network.STA_IF)
        n.active(True)
        n.connect('lakenet', 'keem34&2')
        time.sleep(5)
        upip.install('micropython-uasyncio.core')

if __name__ == "__main__":
    c = waterpumpinstall()
    
    c.upip_uasync()
        
        