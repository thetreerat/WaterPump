# WaterPump
This is a microPython Libary for working with Pumps, Flowmeters, Pressure Sensors, valvues, LED's, and buttons.
do the the memory issuse with my code I have had to move to frozen modules. if you try to load the raw files into flash you will have memory errors. if you need help creating a bin file with the frozen code please see adafruits tutoral at: https://learn.adafruit.com/micropython-basics-loading-modules/frozen-modules?view=all

## server_uasync.py - Simple Server
So that you can access pumps and data remotely. This can be either a remote contoller or a
telnet conncection. This is all in devolpement. 


## uasync.core
This project is in the process implementing asyncio and coroutines. Example_uasyncio/main.py
is a example file that will implement one reley to contoller the pump, a button to turn on and
off the pump, a tri led to give status of the pump. it also will read a 3 wire pressure sensor. 

The simple server at this time will accept connections but dose not do andthing with them. 

This code has only been tested with Adafruit Feather HUZZAH with ESP8266 WiFi.

## uasync
you need to install the __init__.py file from this project into lib/uasyncio folder


# Install Instructions
if running a Adafruit Feather HUZZAH with ESP8266 WiFi make sure to alicate more then 8M of the flash.
Adafruit demo use 8M flash_size as images before 1.8.6 fit fine, this is to small for this
example use something like this:
```python
      esptool.py --port /path/to/port --baud 460800 write_flash --flash_size=32m 0 /path/to/image
``` 

For more then about two modules to work you must byte freeze the code. Please see the tutoral from adafruit if you need help on craeting byte frozen code.

https://learn.adafruit.com/micropython-basics-loading-modules/frozen-modules?view=all

# Modules list

##Leds.py
need text

##pumps.py
need text

##flowMeters.py
need text

##pressure.py
need text

##buttons.py
need text

##server_asyncio.py
need text


