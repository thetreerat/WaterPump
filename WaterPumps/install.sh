#!/bin/bash
erase=0
load=0
firmware="firmware-combined.bin"
main="../ExampleRemote/main.py"
#firmware="esp8266-20170428-v1.8.7-673-g49de9b6.bin"
function usage
{
    echo "usage: install.sh [[-l] [-f file] [-e]  |  [-h] ]"
}

while [ "$1" != "" ]; do
    case $1 in
        -l | --load_firmware )  load=1
                                ;;
        -f | --firmware )       shift
                                firmware=$1
                                ;;
        -m | --main )           shift
                                main=$1
                                ;;
        -e | --erase )          erase=1
                                ;;
        -h | --help )           usage
                                exit
                                ;;
        * )                     usage
                                exit 1
    esac
    shift
done


if [ "$erase" = "1" ]; then                    
    esptool.py --port /dev/tty.SLAB_USBtoUART erase_flash
fi
mv ~/source/vagrant/esp8266-micropython-vagrant/$firmware ~/Iso-images/micropython/ESP8266/.
if [ "$load_firmware" = "1" ]; then
    esptool.py --port /dev/tty.SLAB_USBtoUART --baud 460800 write_flash --flash_size=32m 0 /Users/halc/Iso-images/micropython/ESP8266/$firmware
    echo "puase 5 seconds for controller to settle"
    sleep 5
fi
if [ "$erase" = "1" ]; then
    echo "installing install.py as main.py"
    ampy -p /dev/tty.SLAB_USBtoUART put install.py main.py
    echo "screen will start, reboot controller, it should reboot twice exit with ctrl+a, ctrl+\,Y"
    sleep 3
    screen /dev/tty.SLAB_USBtoUART 115200
    echo "making dir WaterPumps"
    ampy -p /dev/tty.SLAB_USBtoUART mkdir WaterPumps
fi

#ampy -p /dev/tty.SLAB_USBtoUART mkdir lib
#ampy -p /dev/tty.SLAB_USBtoUART mkdir lib/uasyncio
echo "installing main.py from ExampleEvents"
#ampy -p /dev/tty.SLAB_USBtoUART put ../ExampleEvents/main.py main.py
ampy -p /dev/tty.SLAB_USBtoUART put $main main.py
#ampy -p /dev/tty.SLAB_USBtoUART put pressure.py WaterPumps/pressure.py
#ampy -p /dev/tty.SLAB_USBtoUART put flowMeters.py WaterPumps/flowMeters.py
#ampy -p /dev/tty.SLAB_USBtoUART put buttons.py WaterPumps/buttons.py
#echo "installing servers.py"
#ampy -p /dev/tty.SLAB_USBtoUART put servers.py WaterPumps/servers.py
#echo "installing uasyncio core.py"
#ampy -p /dev/tty.SLAB_USBtoUART put ../lib/uasyncio/core.py lib/uasyncio/core.py
#echo "installing uasyncio __init__.py"
#ampy -p /dev/tty.SLAB_USBtoUART put ../lib/uasyncio/__init__.py lib/uasyncio/__init__.py
#echo "installing logging.py"
#ampy -p /dev/tty.SLAB_USBtoUART put ../lib/logging.py lib/logging.py
echo "installing remote.py"
ampy -p /dev/tty.SLAB_USBtoUART put remotes.py WaterPumps/remotes.py
echo "installing monitor.py"
ampy -p /dev/tty.SLAB_USBtoUART put monitors.py WaterPumps/monitors.py
echo "installing contollers.py"
ampy -p /dev/tty.SLAB_USBtoUART put controllers.py WaterPumps/controllers.py
echo "installing remotefucn.py"
ampy -p /dev/tty.SLAB_USBtoUART put ../ExampleRemote/remotefunc.py remotefunc.py