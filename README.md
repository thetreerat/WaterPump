# WaterPump
This is a microPython Libary for working with Pumps, Flowmeters, Pressure Sensors, valvues, LED's, and buttons.

## Simple Server
So that you can access pumps and data remotely. This can be either a remote contoller or a telnet conncection. This is 
all in devolpement and not considered stable yet. 

## uasync.core
This project is in the process implementing asyncio and coroutines. Example_uasyncio/main.py is a example file that will implement one reley to contoller the pump, a button to turn on and off the pump, a tri led to give status of the pump. it also will read a 3 wire pressure sensor. 

The simple server at this time will accept connections but dose not do andthing with them. 

This code has only been tested with Adafruit Feather HUZZAH with ESP8266 WiFi.

# Install Instructions
must load the micropython libary "micropython-uasyncio.core", and be running 1.8.5 or later
to install uasyncio.core form the board:
```python
      import upip
      upip.install("micropython_uasyncio.core")  # this fails with 8m of flash size 
```
if running a Adafruit Feather HUZZAH with ESP8266 WiFi make sure to alicate more then 8M of the flash
original how to remcommend a flash_size=8m this is to small for this example use something like this:
```python
      esptool.py --port /path/to/port --baud 460800 write_flash --flash_size=32m 0 /path/to/image
``` 
 
you next need to copy the folder and all files in /WaterPumps from this project to your board. If you use 
the webrepl or ampy to copy all the files in the /WaterPumps folder to the root. you can run:
```python
     install_waterpump.py
```
This will create folder Waterpumps if it is not there and copy any of modules at root to the folder. 
