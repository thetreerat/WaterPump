# WaterPump
This is a microPython Libary for working with Pumps, Flowmeters, Pressure Sensors, valvues, LED's, and buttons.

## Simple Server
So that you can access pumps and data remotely. This can be either a remote contoller or a
telnet conncection. This is all in devolpement and not considered stable yet. 

## uasync.core
This project is in the process implementing asyncio and coroutines. Example_uasyncio/main.py
is a example file that will implement one reley to contoller the pump, a button to turn on and
off the pump, a tri led to give status of the pump. it also will read a 3 wire pressure sensor. 

The simple server at this time will accept connections but dose not do andthing with them. 

This code has only been tested with Adafruit Feather HUZZAH with ESP8266 WiFi.

# Install Instructions
if running a Adafruit Feather HUZZAH with ESP8266 WiFi make sure to alicate more then 8M of the flash.
Adafruit demo use 8M flash_size as images before 1.8.6 fit fine, this is to small for this
example use something like this:
```python
      esptool.py --port /path/to/port --baud 460800 write_flash --flash_size=32m 0 /path/to/image
``` 

This libary uses  micropython libary "micropython-uasyncio.core", and your micropython board needs to
be running 1.8.5 or later to install uasyncio.core form the board:
```python
import upip
upip.install("micropython-uasyncio.core")  # this fails with 8m of flash size 
```

I have modified the __init__.py from the micropython-uasyncio libary. This need to be copied from the

Waterpump/__init__.py to /lib/uasyncio/__init__.py

you next need to copy the modules from Waterpump/WaterPumps from this project to your board in
WaterPumps/*. If you use the webrepl or ampy to copy all the files in the /WaterPumps
folder to the root. you can run:
```python
     install_waterpump.py
```
This will create folder Waterpumps if it is not there and copy any of modules at root to the folder. 
