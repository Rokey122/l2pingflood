# l2pingflood

Simple python script to preform a l2ping flood attack. It uses bluetoothctl to scan for nearby bluetooth devices and saves them so that you can select which ones to attack. Was tested on a bt speaker and works well.

# Usage

**Works only on linux with sudo privileges**

In a terminal window run:
```
sudo python3 l2pingflood.py
```
After the script finishes scanning, you can select which devices/devices you want to attack, separated by comma, eg. 2,3,5 or you can type 'all' to attack all devices. You can also choose the amount of threads to use to attack a device (default is 100). Stop the script with Ctrl-C.

# Requirements

BlueZ (bluetoothctl)

Bluetooth hci device (default is hci0, but if you use eg. hci1, change it in the script)

Sudo privileges

Python3


