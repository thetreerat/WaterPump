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
        if not 'WaterPumps' in os.listdir():
            os.mkdir('WaterPumps')
            if not 'WaterPumps' in sys.path:
                sys.path.append('WaterPumps')
        else:
            print('WaterPumps exists')
        #rootFiles = os.listdir()
        files = ['__init__.py',
                'pumps.py',
                'servers.py',
                'flowMeters.py',
                'buttons.py',
                'leds.py',
                'wifi.py',
                'server_uasyncio.py',
                'pressure.py']
        for f in files:
            try:
                os.rename(f, '/WaterPumps/' + f)
                print('''found %s moved.''' % (f))
            except OSError:
                missingfiles.append(f)
                #print('Error with file %s' % (f))
        if not missingfiles==[]:
            print('files missing: ')
            for f in missingfiles:
                print(f)