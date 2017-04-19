import os
try:
    os.mkdir('WaterPumps')
except OSError:
    print('WaterPumps exists')
#rootFiles = os.listdir()
files = ['__init__.py', 'pumps.py', 'servers.py', 'flowMeters.py', 'buttons.py', 'leds.py','wifi.py']
for f in files:
#    for r in rootfiles:
#        if r==f:        
    try:
        os.rename(f, '/WaterPumps/' + f)
    except OSError:
        print('Error with file %s' % (f))