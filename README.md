# WaterPump
This is a microPython Libary for working with Pumps, Flowmeters, Pressure Sensors, valves, LED's, and buttons.
do the the memory issuse with my code I have had to move to frozen modules. if you try to load the raw files into flash you will have memory errors. 

# Install Instructions
if running a Adafruit Feather HUZZAH with ESP8266 WiFi make sure to alicate more then 8M of the flash.
Adafruit demo use 8M flash_size as images before 1.8.6 fit fine, this is to small for this
example use something like this:
```python
      esptool.py --port /path/to/port --baud 460800 write_flash --flash_size=32m 0 /path/to/image
``` 

For more then about two modules to work you must byte freeze the code. Please see the tutoral from adafruit if you need help on craeting byte frozen code.

https://learn.adafruit.com/micropython-basics-loading-modules/frozen-modules?view=all

## uasync.core
This project is in the process implementing asyncio and coroutines. Example_uasyncio/main.py
is a example file that will implement one reley to contoller the pump, a button to turn on and
off the pump, a tri led to give status of the pump. it also will read a 3 wire pressure sensor. 

The simple server at this time will accept connections but dose not do andthing with them. 

This code has only been tested with Adafruit Feather HUZZAH with ESP8266 WiFi.
*** do to memory issues I install this file with the frozen code from my project
## uasync
you need to install the __init__.py file from this project into lib/uasyncio folded

*** do to memory issues I install this file with the frozen code from my project

## Logging.py
This is required by uasync 
*** do to memory issues I install this file with the frozen code from my project

## server.py - Simple Server
So that you can access pumps and data remotely. This can be either a remote contoller or a
telnet conncection. This is all in devolpement. 


# Modules list

## Leds.py
need text

## pumps.py
This pump module controls a reley to turn on and off the pump. 
Events
      

## flowMeters.py
need text

## pressure.py
need text

## buttons.py
need text




