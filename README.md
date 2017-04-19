# WaterPump
This is a microPython Libary for working with Pumps,Flowmeters,Pressure Sensors,LED's, and buttons. There is a simple server
also so that you can access pumps and data remotely. This can be either a remote contoler or a telnet conncection. This is 
all in devolpement and not considered stable yet. 

This project is in the process implementing asyncio and coroutines. Example_uasyncio/main.py uses the update class files. 
This code has only been tested with Adafruit Feather HUZZAH with ESP8266 WiFi.   

# Install Instructions
must load the micropython libary "micropython-uasyncio.core", and be running 1.8.5 or later
to install uasyncio.core form the board:
      import upip
      upip.install("micropython_uasyncio.core")  # this fails with 8m of flash size on 1.8.5 and later

if running a Adafruit Feather HUZZAH with ESP8266 WiFi make sure to alicate more then 8M of the flash
original how to remcommend a flash_size=8m this is to small for this example use something like this:
      esptool.py --port /path/to/port --baud 460800 write_flash --flash_size=32m 0 /path/to/image
 
 
you next need to copy the folder and all files in /WaterPumps from this project to your board.

if you use wthe webreple to copy all the files in the /WaterPumps folder to the root. you can run:
     install_waterpump.py
This will create folder Waterpumps is not there and copy any of modules at root to the folder. 
