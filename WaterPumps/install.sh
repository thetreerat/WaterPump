#!/bin/bash
esptool.py --port /dev/tty.SLAB_USBtoUART erase_flash
mv ~/source/vagrant/esp8266-micropython-vagrant/firmware-combined.bin ~/Iso-images/micropython/ESP8266/.
#esptool.py --port /dev/tty.SLAB_USBtoUART --baud 460800 write_flash --flash_size=32m 0 /Users/halc/Iso-images/micropython/ESP8266/firmware-combined.bin
esptool.py --port /dev/tty.SLAB_USBtoUART --baud 460800 write_flash --flash_size=32m 0 /Users/halc/Iso-images/micropython/ESP8266/esp8266-20170428-v1.8.7-673-g49de9b6.bin
read -p "Press [Enter] key"
ampy -p /dev/tty.SLAB_USBtoUART put install_waterpump.py main.py
read -p "Press [Enter] key"
#ampy -p /dev/tty.SLAB_USBtoUART run install_waterpump.py
ampy -p /dev/tty.SLAB_USBtoUART mkdir WaterPumps
ampy -p /dev/tty.SLAB_USBtoUART put ../lib/uasyncio/__init__.py lib/uasyncio/__init__.py
ampy -p /dev/tty.SLAB_USBtoUART put ../Example_uasyncio/main.py main.py
#ampy -p /dev/tty.SLAB_USBtoUART put pressure.py WaterPumps/pressure.py
ampy -p /dev/tty.SLAB_USBtoUART put flowMeters.py WaterPumps/flowMeters.py