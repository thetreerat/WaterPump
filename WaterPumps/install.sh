#!/bin/bash
esptool.py --port /dev/tty.SLAB_USBtoUART erase_flash
mv ~/source/vagrant/esp8266-micropython-vagrant/firmware-combined.bin ~/Iso-images/micropython/ESP8266/.
esptool.py --port /dev/tty.SLAB_USBtoUART --baud 460800 write_flash --flash_size=32m 0 /Users/halc/Iso-images/micropython/ESP8266/firmware-combined.bin
#esptool.py --port /dev/tty.SLAB_USBtoUART --baud 460800 write_flash --flash_size=32m 0 /Users/halc/Iso-images/micropython/ESP8266/esp8266-20170428-v1.8.7-673-g49de9b6.bin
echo "puase 5 seconds for controller to settle"
sleep 5
echo "installing install.py as main.py"
ampy -p /dev/tty.SLAB_USBtoUART put install.py main.py
echo "screen will start, reboot controller, it should reboot twice exit with ctrl+a, ctrl+\,Y"
ampy -p /dev/tty.SLAB_USBtoUART reset
sleep 3
#ampy -p /dev/tty.SLAB_USBtoUART run install_waterpump.py
screen /dev/tty.SLAB_USBtoUART 115200
echo "making dir WaterPumps"
ampy -p /dev/tty.SLAB_USBtoUART mkdir WaterPumps
#ampy -p /dev/tty.SLAB_USBtoUART mkdir lib
#ampy -p /dev/tty.SLAB_USBtoUART mkdir lib/uasyncio
echo "installing main.py from ExampleEvents"
ampy -p /dev/tty.SLAB_USBtoUART put ../ExampleEvents/main.py main.py
#ampy -p /dev/tty.SLAB_USBtoUART put pressure.py WaterPumps/pressure.py
#ampy -p /dev/tty.SLAB_USBtoUART put flowMeters.py WaterPumps/flowMeters.py
#ampy -p /dev/tty.SLAB_USBtoUART put buttons.py WaterPumps/buttons.py
ampy -p /dev/tty.SLAB_USBtoUART put server_uasyncio.py WaterPumps/server_uasyncio.py
#echo "installing uasyncio core.py"
#ampy -p /dev/tty.SLAB_USBtoUART put ../lib/uasyncio/core.py lib/uasyncio/core.py
#echo "installing uasyncio __init__.py"
#ampy -p /dev/tty.SLAB_USBtoUART put ../lib/uasyncio/__init__.py lib/uasyncio/__init__.py
#echo "installing logging.py"
#ampy -p /dev/tty.SLAB_USBtoUART put ../lib/logging.py lib/logging.py