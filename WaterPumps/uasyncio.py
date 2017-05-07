from os import listdir        
import upip
if not 'lib' in listdir():
    upip.install('micropython-uasyncio.core')
from os import remove
remove('main.py')
print('finished, reboot controller')